from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .. import models, schemas, database

router = APIRouter(prefix="/api/assets", tags=["Assets"])


# Feature: Create a new physical asset
# POST /api/assets
# DB: INSERT into assets table
@router.post("/", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(database.get_db)):
    # Check for duplicate asset_tag
    existing = db.query(models.Asset).filter(models.Asset.asset_tag == asset.asset_tag).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Asset with tag '{asset.asset_tag}' already exists.")
    db_asset = models.Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


# Feature: Search for an asset by its unique tag
# GET /api/assets/tag/{asset_tag}
# DB: SELECT from assets WHERE asset_tag = ?
@router.get("/tag/{asset_tag}", response_model=schemas.Asset)
def get_asset_by_tag(asset_tag: str, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).filter(models.Asset.asset_tag == asset_tag).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    return asset


# Feature: List all assets (with optional status filter)
# GET /api/assets?status=In Stock
# DB: SELECT * from assets [WHERE status = ?]
@router.get("/", response_model=List[schemas.Asset])
def list_assets(
    status: Optional[str] = Query(None, description="Filter by status (e.g., 'In Stock', 'Assigned')"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Asset)
    if status:
        query = query.filter(models.Asset.status == status)
    return query.offset(skip).limit(limit).all()


# Feature: View detailed specifications of a specific asset
# GET /api/assets/{id}
# DB: SELECT * from assets WHERE id = ?
@router.get("/{asset_id}", response_model=schemas.Asset)
def get_asset(asset_id: int, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    return asset


# Feature: Update asset metadata (e.g., condition or notes)
# PATCH /api/assets/{id}
# DB: UPDATE assets SET ... WHERE id = ?
@router.patch("/{asset_id}", response_model=schemas.Asset)
def update_asset(asset_id: int, asset_update: schemas.AssetUpdate, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    update_data = asset_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asset, key, value)
    asset.last_updated_at = datetime.utcnow()
    db.commit()
    db.refresh(asset)
    return asset


# Feature: Decommission or retire an asset
# DELETE /api/assets/{id}
# DB: UPDATE assets SET status = 'Retired' WHERE id = ?
@router.delete("/{asset_id}")
def retire_asset(asset_id: int, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    asset.status = "Retired"
    asset.last_updated_at = datetime.utcnow()
    db.commit()
    return {"message": f"Asset '{asset.asset_name}' (ID: {asset_id}) has been retired."}


# Feature: View the full assignment history of a specific asset
# GET /api/assets/{id}/history
# DB: SELECT * from asset_assignment_history WHERE asset_id = ? ORDER BY assigned_date DESC
@router.get("/{asset_id}/history", response_model=List[schemas.AssetAssignmentHistory])
def get_asset_history(asset_id: int, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    history = (
        db.query(models.AssetAssignmentHistory)
        .filter(models.AssetAssignmentHistory.asset_id == asset_id)
        .order_by(models.AssetAssignmentHistory.assigned_date.desc())
        .all()
    )
    return history


# Feature: View all maintenance logs for an asset
# GET /api/assets/{id}/maintenance
# DB: SELECT * from maintenance_logs WHERE asset_id = ?
@router.get("/{asset_id}/maintenance", response_model=List[schemas.MaintenanceLog])
def get_asset_maintenance(asset_id: int, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    logs = (
        db.query(models.MaintenanceLog)
        .filter(models.MaintenanceLog.asset_id == asset_id)
        .all()
    )
    return logs
