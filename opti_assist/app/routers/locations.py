from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/locations", tags=["Locations"])


@router.post("/", response_model=schemas.Location, status_code=201)
def create_location(location: schemas.LocationCreate, db: Session = Depends(database.get_db)):
    """
    Register a new physical location/site.
    """
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


@router.get("/", response_model=List[schemas.Location])
def list_locations(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Retrieve a list of all registered locations.
    """
    return db.query(models.Location).offset(skip).limit(limit).all()


@router.get("/{location_id}", response_model=schemas.Location)
def get_location(location_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve details of a single location by its ID.
    """
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found.")
    return loc


@router.patch("/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, loc_update: schemas.LocationUpdate, db: Session = Depends(database.get_db)):
    """
    Update an existing location's information.
    """
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found.")
    
    for key, value in loc_update.dict(exclude_unset=True).items():
        setattr(loc, key, value)
    
    db.commit()
    db.refresh(loc)
    return loc


@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a location from the system.
    """
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found.")
    
    db.delete(loc)
    db.commit()
    return {"message": f"Location '{loc.site_name}' (ID: {location_id}) deleted."}
