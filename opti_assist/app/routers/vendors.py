from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/vendors", tags=["Vendors"])


# Feature: Add a new vendor
# POST /api/vendors
# DB: INSERT into vendors table
@router.post("/", response_model=schemas.Vendor)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(database.get_db)):
    db_vendor = models.Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


# Feature: View all vendors
# GET /api/vendors
# DB: SELECT * from vendors
@router.get("/", response_model=List[schemas.Vendor])
def list_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Vendor).offset(skip).limit(limit).all()


# Feature: View a single vendor by ID
# GET /api/vendors/{id}
# DB: SELECT * from vendors WHERE id = ?
@router.get("/{vendor_id}", response_model=schemas.Vendor)
def get_vendor(vendor_id: int, db: Session = Depends(database.get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    return vendor


# Feature: Update a vendor
# PATCH /api/vendors/{id}
# DB: UPDATE vendors SET ... WHERE id = ?
@router.patch("/{vendor_id}", response_model=schemas.Vendor)
def update_vendor(vendor_id: int, vendor_update: schemas.VendorUpdate, db: Session = Depends(database.get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    for key, value in vendor_update.dict(exclude_unset=True).items():
        setattr(vendor, key, value)
    db.commit()
    db.refresh(vendor)
    return vendor


# Feature: Delete a vendor
# DELETE /api/vendors/{id}
# DB: DELETE from vendors WHERE id = ?
@router.delete("/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(database.get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    db.delete(vendor)
    db.commit()
    return {"message": f"Vendor '{vendor.vendor_name}' (ID: {vendor_id}) deleted."}
