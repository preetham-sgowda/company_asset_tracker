from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/vendors", tags=["Vendors"])


@router.post("/", response_model=schemas.Vendor, status_code=201)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(database.get_db)):
    """
    Register a new third-party vendor.
    """
    db_vendor = models.Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


@router.get("/", response_model=List[schemas.Vendor])
def list_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Retrieve a list of all vendors.
    """
    return db.query(models.Vendor).offset(skip).limit(limit).all()


@router.get("/{vendor_id}", response_model=schemas.Vendor)
def get_vendor(vendor_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve details of a single vendor by its ID.
    """
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    return vendor


@router.patch("/{vendor_id}", response_model=schemas.Vendor)
def update_vendor(vendor_id: int, vendor_update: schemas.VendorUpdate, db: Session = Depends(database.get_db)):
    """
    Update an existing vendor's information.
    """
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    
    for key, value in vendor_update.dict(exclude_unset=True).items():
        setattr(vendor, key, value)
    
    db.commit()
    db.refresh(vendor)
    return vendor


@router.delete("/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a vendor from the system.
    """
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    
    db.delete(vendor)
    db.commit()
    return {"message": f"Vendor '{vendor.vendor_name}' (ID: {vendor_id}) deleted."}
