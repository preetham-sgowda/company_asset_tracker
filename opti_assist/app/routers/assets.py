from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .. import models, schemas, database

router = APIRouter(prefix="/api/assets", tags=["Assets"])


@router.post("/", response_model=schemas.Asset, status_code=201)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(database.get_db)):
    """
    Register a new physical asset in the system.
    
    - **asset_tag**: Unique identifier (barcode/RFID).
    - **status**: Defaults to 'In Stock'.
    """
    # Check for duplicate asset_tag
    existing = db.query(models.Asset).filter(models.Asset.asset_tag == asset.asset_tag).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Asset with tag '{asset.asset_tag}' already exists.")
    
    db_asset = models.Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.get("/tag/{asset_tag}", response_model=schemas.Asset)
def get_asset_by_tag(asset_tag: str, db: Session = Depends(database.get_db)):
    """
    Retrieve asset details using its unique asset tag.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_tag == asset_tag).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    return asset


@router.get("/", response_model=List[schemas.Asset])
def list_assets(
    status: Optional[str] = Query(None, description="Filter by status (e.g., 'In Stock', 'Assigned')"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """
    List all assets with optional filtering by status and pagination support.
    """
    query = db.query(models.Asset)
    if status:
        query = query.filter(models.Asset.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{asset_id}", response_model=schemas.Asset)
def get_asset(asset_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve full specifications of a specific asset by its database ID.
    """
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    return asset


@router.patch("/{asset_id}", response_model=schemas.Asset)
def update_asset(asset_id: int, asset_update: schemas.AssetUpdate, db: Session = Depends(database.get_db)):
    """
    Update metadata for an existing asset.
    Allows partial updates for condition, notes, location, etc.
    """
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


@router.delete("/{asset_id}")
def retire_asset(asset_id: int, db: Session = Depends(database.get_db)):
    """
    Decommission or retire an asset.
    Changes the asset status to 'Retired' rather than performing a hard deletion.
    """
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    
    asset.status = "Retired"
    asset.last_updated_at = datetime.utcnow()
    db.commit()
    return {"message": f"Asset '{asset.asset_name}' (ID: {asset_id}) has been retired."}


@router.get("/{asset_id}/history", response_model=List[schemas.AssetAssignmentHistory])
def get_asset_history(asset_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve the complete assignment and movement history for a specific asset.
    Ordered by assignment date (descending).
    """
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


@router.get("/{asset_id}/maintenance", response_model=List[schemas.MaintenanceLog])
def get_asset_maintenance(asset_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all maintenance and repair logs associated with a specific asset.
    """
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    
    logs = (
        db.query(models.MaintenanceLog)
        .filter(models.MaintenanceLog.asset_id == asset_id)
        .all()
    )
    return logs
