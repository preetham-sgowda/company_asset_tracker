from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from . import models, schemas, database

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Opti Assist API", description="Enterprise Asset Management System API")

# Dependency
def get_db():
    return database.get_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to Opti Assist API"}

@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(database.get_db)):
    try:
        # Try to execute a simple query to check DB connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# --- Basic CRUD Endpoints (Examples) ---

@app.post("/departments/", response_model=schemas.Department, tags=["Departments"])
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(database.get_db)):
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@app.get("/departments/", response_model=List[schemas.Department], tags=["Departments"])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    departments = db.query(models.Department).offset(skip).limit(limit).all()
    return departments

@app.get("/assets/", response_model=List[schemas.Asset], tags=["Assets"])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    assets = db.query(models.Asset).offset(skip).limit(limit).all()
    return assets
