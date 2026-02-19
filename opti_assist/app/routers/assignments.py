from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import models, schemas, database

router = APIRouter(prefix="/api", tags=["Assignments"])


# Feature: Assign an in-stock asset to an employee
# POST /api/assignments
# DB: INSERT into asset_assignment_history; UPDATE assets SET current_employee_id, status = 'Assigned'
@router.post("/assignments", response_model=schemas.AssetAssignmentHistory)
def assign_asset(request: schemas.AssignAssetRequest, db: Session = Depends(database.get_db)):
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


# Feature: Record the return of an asset to inventory
# POST /api/returns
# DB: UPDATE asset_assignment_history SET returned_date; UPDATE assets SET current_employee_id = NULL, status = 'In Stock'
@router.post("/returns")
def return_asset(request: schemas.ReturnAssetRequest, db: Session = Depends(database.get_db)):
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
