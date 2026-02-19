from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/locations", tags=["Locations"])


# Feature: Add a new location
# POST /api/locations
# DB: INSERT into locations table
@router.post("/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(database.get_db)):
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


# Feature: View all locations
# GET /api/locations
# DB: SELECT * from locations
@router.get("/", response_model=List[schemas.Location])
def list_locations(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Location).offset(skip).limit(limit).all()


# Feature: View a single location by ID
# GET /api/locations/{id}
# DB: SELECT * from locations WHERE id = ?
@router.get("/{location_id}", response_model=schemas.Location)
def get_location(location_id: int, db: Session = Depends(database.get_db)):
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found.")
    return loc


# Feature: Update a location
# PATCH /api/locations/{id}
# DB: UPDATE locations SET ... WHERE id = ?
@router.patch("/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, loc_update: schemas.LocationUpdate, db: Session = Depends(database.get_db)):
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found.")
    for key, value in loc_update.dict(exclude_unset=True).items():
        setattr(loc, key, value)
    db.commit()
    db.refresh(loc)
    return loc


# Feature: Delete a location
# DELETE /api/locations/{id}
# DB: DELETE from locations WHERE id = ?
@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(database.get_db)):
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found.")
    db.delete(loc)
    db.commit()
    return {"message": f"Location '{loc.site_name}' (ID: {location_id}) deleted."}
