from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/asset-categories", tags=["Asset Categories"])


# Feature: Add a new asset category
# POST /api/asset-categories
# DB: INSERT into asset_categories table
@router.post("/", response_model=schemas.AssetCategory)
def create_category(category: schemas.AssetCategoryCreate, db: Session = Depends(database.get_db)):
    db_category = models.AssetCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Feature: View all asset categories
# GET /api/asset-categories
# DB: SELECT * from asset_categories
@router.get("/", response_model=List[schemas.AssetCategory])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.AssetCategory).offset(skip).limit(limit).all()


# Feature: View a single category by ID
# GET /api/asset-categories/{id}
# DB: SELECT * from asset_categories WHERE id = ?
@router.get("/{category_id}", response_model=schemas.AssetCategory)
def get_category(category_id: int, db: Session = Depends(database.get_db)):
    cat = db.query(models.AssetCategory).filter(models.AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Asset category not found.")
    return cat


# Feature: Group assets by category
# GET /api/asset-categories/{id}/assets
# DB: SELECT * from assets WHERE category_id = ?
@router.get("/{category_id}/assets", response_model=List[schemas.Asset])
def get_assets_by_category(category_id: int, db: Session = Depends(database.get_db)):
    cat = db.query(models.AssetCategory).filter(models.AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Asset category not found.")
    assets = db.query(models.Asset).filter(models.Asset.category_id == category_id).all()
    return assets


# Feature: Update an asset category
# PATCH /api/asset-categories/{id}
# DB: UPDATE asset_categories SET ... WHERE id = ?
@router.patch("/{category_id}", response_model=schemas.AssetCategory)
def update_category(category_id: int, cat_update: schemas.AssetCategoryUpdate, db: Session = Depends(database.get_db)):
    cat = db.query(models.AssetCategory).filter(models.AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Asset category not found.")
    for key, value in cat_update.dict(exclude_unset=True).items():
        setattr(cat, key, value)
    db.commit()
    db.refresh(cat)
    return cat


# Feature: Delete an asset category
# DELETE /api/asset-categories/{id}
# DB: DELETE from asset_categories WHERE id = ?
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(database.get_db)):
    cat = db.query(models.AssetCategory).filter(models.AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Asset category not found.")
    db.delete(cat)
    db.commit()
    return {"message": f"Category '{cat.category_name}' (ID: {category_id}) deleted."}
