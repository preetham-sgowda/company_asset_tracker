from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/asset-categories", tags=["Asset Categories"])


@router.post("/", response_model=schemas.AssetCategory, status_code=201)
def create_category(category: schemas.AssetCategoryCreate, db: Session = Depends(database.get_db)):
    """
    Create a new asset category (e.g., Laptops, Furniture).
    """
    db_category = models.AssetCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/", response_model=List[schemas.AssetCategory])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Retrieve a list of all asset categories.
    """
    return db.query(models.AssetCategory).offset(skip).limit(limit).all()


@router.get("/{category_id}", response_model=schemas.AssetCategory)
def get_category(category_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve details of a single category by its ID.
    """
    cat = db.query(models.AssetCategory).filter(models.AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Asset category not found.")
    return cat


@router.get("/{category_id}/assets", response_model=List[schemas.Asset])
def get_assets_by_category(category_id: int, db: Session = Depends(database.get_db)):
    """
    List all assets belonging to a specific category.
    """
    cat = db.query(models.AssetCategory).filter(models.AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Asset category not found.")
    
    assets = db.query(models.Asset).filter(models.Asset.category_id == category_id).all()
    return assets


@router.patch("/{category_id}", response_model=schemas.AssetCategory)
def update_category(category_id: int, cat_update: schemas.AssetCategoryUpdate, db: Session = Depends(database.get_db)):
    """
    Update an existing asset category.
    """
    cat = db.query(models.AssetCategory).filter(models.AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Asset category not found.")
    
    for key, value in cat_update.dict(exclude_unset=True).items():
        setattr(cat, key, value)
    
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(database.get_db)):
    """
    Delete an asset category from the system.
    """
    cat = db.query(models.AssetCategory).filter(models.AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Asset category not found.")
    
    db.delete(cat)
    db.commit()
    return {"message": f"Category '{cat.category_name}' (ID: {category_id}) deleted."}
