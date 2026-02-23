from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/maintenance-logs", tags=["Maintenance"])


@router.post("/", response_model=schemas.MaintenanceLog, status_code=201)
def create_maintenance_log(log: schemas.MaintenanceLogCreate, db: Session = Depends(database.get_db)):
    """
    Log a new maintenance event for a specific asset.
    """
    # Validate asset exists
    asset = db.query(models.Asset).filter(models.Asset.id == log.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    
    db_log = models.MaintenanceLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("/", response_model=List[schemas.MaintenanceLog])
def list_maintenance_logs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    List all maintenance logs across all assets.
    """
    return db.query(models.MaintenanceLog).offset(skip).limit(limit).all()


@router.get("/{log_id}", response_model=schemas.MaintenanceLog)
def get_maintenance_log(log_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve details of a single maintenance log by its ID.
    """
    log = db.query(models.MaintenanceLog).filter(models.MaintenanceLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found.")
    return log


@router.patch("/{log_id}", response_model=schemas.MaintenanceLog)
def update_maintenance_log(log_id: int, log_update: schemas.MaintenanceLogUpdate, db: Session = Depends(database.get_db)):
    """
    Update an existing maintenance log.
    """
    log = db.query(models.MaintenanceLog).filter(models.MaintenanceLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found.")
    
    for key, value in log_update.dict(exclude_unset=True).items():
        setattr(log, key, value)
    
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}")
def delete_maintenance_log(log_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a specific maintenance log.
    """
    log = db.query(models.MaintenanceLog).filter(models.MaintenanceLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found.")
    
    db.delete(log)
    db.commit()
    return {"message": f"Maintenance log (ID: {log_id}) deleted."}
