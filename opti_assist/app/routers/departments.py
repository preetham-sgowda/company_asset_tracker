from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/departments", tags=["Departments"])


@router.post("/", response_model=schemas.Department, status_code=201)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(database.get_db)):
    """
    Create a new organizational department.
    """
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.get("/", response_model=List[schemas.Department])
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Retrieve a list of all departments.
    """
    return db.query(models.Department).offset(skip).limit(limit).all()


@router.get("/{department_id}", response_model=schemas.Department)
def get_department(department_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve details of a single department by its ID.
    """
    dept = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found.")
    return dept


@router.patch("/{department_id}", response_model=schemas.Department)
def update_department(department_id: int, dept_update: schemas.DepartmentUpdate, db: Session = Depends(database.get_db)):
    """
    Update an existing department's information.
    """
    dept = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found.")
    
    for key, value in dept_update.dict(exclude_unset=True).items():
        setattr(dept, key, value)
    
    db.commit()
    db.refresh(dept)
    return dept


@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a department from the system.
    """
    dept = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found.")
    
    db.delete(dept)
    db.commit()
    return {"message": f"Department '{dept.name}' (ID: {department_id}) deleted."}
