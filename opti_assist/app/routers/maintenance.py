from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/maintenance-logs", tags=["Maintenance"])


# Feature: Log a maintenance event
# POST /api/maintenance-logs
# DB: INSERT into maintenance_logs table
@router.post("/", response_model=schemas.MaintenanceLog)
def create_maintenance_log(log: schemas.MaintenanceLogCreate, db: Session = Depends(database.get_db)):
    # Validate asset exists
    asset = db.query(models.Asset).filter(models.Asset.id == log.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")
    db_log = models.MaintenanceLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


# Feature: View all maintenance logs
# GET /api/maintenance-logs
# DB: SELECT * from maintenance_logs
@router.get("/", response_model=List[schemas.MaintenanceLog])
def list_maintenance_logs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.MaintenanceLog).offset(skip).limit(limit).all()


# Feature: View a single maintenance log by ID
# GET /api/maintenance-logs/{id}
# DB: SELECT * from maintenance_logs WHERE id = ?
@router.get("/{log_id}", response_model=schemas.MaintenanceLog)
def get_maintenance_log(log_id: int, db: Session = Depends(database.get_db)):
    log = db.query(models.MaintenanceLog).filter(models.MaintenanceLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found.")
    return log


# Feature: Update a maintenance log
# PATCH /api/maintenance-logs/{id}
# DB: UPDATE maintenance_logs SET ... WHERE id = ?
@router.patch("/{log_id}", response_model=schemas.MaintenanceLog)
def update_maintenance_log(log_id: int, log_update: schemas.MaintenanceLogUpdate, db: Session = Depends(database.get_db)):
    log = db.query(models.MaintenanceLog).filter(models.MaintenanceLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found.")
    for key, value in log_update.dict(exclude_unset=True).items():
        setattr(log, key, value)
    db.commit()
    db.refresh(log)
    return log


# Feature: Delete a maintenance log
# DELETE /api/maintenance-logs/{id}
# DB: DELETE from maintenance_logs WHERE id = ?
@router.delete("/{log_id}")
def delete_maintenance_log(log_id: int, db: Session = Depends(database.get_db)):
    log = db.query(models.MaintenanceLog).filter(models.MaintenanceLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found.")
    db.delete(log)
    db.commit()
    return {"message": f"Maintenance log (ID: {log_id}) deleted."}
