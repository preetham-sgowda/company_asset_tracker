from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import models, schemas, database

router = APIRouter(prefix="/api", tags=["Assignments"])


@router.post("/assignments", response_model=schemas.AssetAssignmentHistory, status_code=201)
def assign_asset(request: schemas.AssignAssetRequest, db: Session = Depends(database.get_db)):
    """
    Assign an 'In Stock' asset to an active employee.
    
    - **asset_id**: The ID of the asset to be assigned.
    - **employee_id**: The ID of the employee receiving the asset.
    - **assigned_by_admin_id**: Optional ID of the administrator performing the assignment.
    
    This endpoint creates a new assignment history record and updates the asset's status and current holder.
    """
    # Validate asset exists
    asset = db.query(models.Asset).filter(models.Asset.id == request.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    
    if asset.status == "Assigned":
        raise HTTPException(status_code=400, detail=f"Asset '{asset.asset_name}' is already assigned. Return it first.")
    
    if asset.status == "Retired":
        raise HTTPException(status_code=400, detail=f"Asset '{asset.asset_name}' is retired and cannot be assigned.")

    # Validate employee exists and is active
    employee = db.query(models.Employee).filter(models.Employee.id == request.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    if employee.employment_status != "Active":
        raise HTTPException(status_code=400, detail=f"Employee '{employee.first_name} {employee.last_name}' is not active.")

    # Create assignment history record
    assignment = models.AssetAssignmentHistory(
        asset_id=request.asset_id,
        employee_id=request.employee_id,
        assigned_date=datetime.utcnow(),
        assigned_by_admin_id=request.assigned_by_admin_id,
        notes=request.notes,
    )
    db.add(assignment)

    # Update the asset
    asset.current_employee_id = request.employee_id
    asset.status = "Assigned"
    asset.last_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(assignment)
    return assignment


@router.post("/returns")
def return_asset(request: schemas.ReturnAssetRequest, db: Session = Depends(database.get_db)):
    """
    Record the return of an assigned asset back to inventory.
    
    - **asset_id**: The ID of the asset being returned.
    
    This marks the current assignment as completed (sets returned_date) and resets the asset's status to 'In Stock'.
    """
    # Validate asset exists
    asset = db.query(models.Asset).filter(models.Asset.id == request.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    
    if asset.status != "Assigned":
        raise HTTPException(status_code=400, detail=f"Asset '{asset.asset_name}' is not currently assigned.")

    # Find the open assignment record (no returned_date)
    assignment = (
        db.query(models.AssetAssignmentHistory)
        .filter(
            models.AssetAssignmentHistory.asset_id == request.asset_id,
            models.AssetAssignmentHistory.returned_date.is_(None),
        )
        .first()
    )
    
    if assignment:
        assignment.returned_date = datetime.utcnow()
        if request.notes:
            assignment.notes = (assignment.notes or "") + f" | Return note: {request.notes}"

    # Update the asset
    asset.current_employee_id = None
    asset.status = "In Stock"
    asset.last_updated_at = datetime.utcnow()

    db.commit()
    return {"message": f"Asset '{asset.asset_name}' (ID: {request.asset_id}) has been returned to inventory."}
