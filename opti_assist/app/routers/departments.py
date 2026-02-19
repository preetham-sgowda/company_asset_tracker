from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database

router = APIRouter(prefix="/api/departments", tags=["Departments"])


# Feature: Add a new department
# POST /api/departments
# DB: INSERT into departments table
@router.post("/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(database.get_db)):
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


# Feature: View all departments
# GET /api/departments
# DB: SELECT * from departments
@router.get("/", response_model=List[schemas.Department])
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Department).offset(skip).limit(limit).all()


# Feature: View a single department by ID
# GET /api/departments/{id}
# DB: SELECT * from departments WHERE id = ?
@router.get("/{department_id}", response_model=schemas.Department)
def get_department(department_id: int, db: Session = Depends(database.get_db)):
    dept = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found.")
    return dept


# Feature: Update a department
# PATCH /api/departments/{id}
# DB: UPDATE departments SET ... WHERE id = ?
@router.patch("/{department_id}", response_model=schemas.Department)
def update_department(department_id: int, dept_update: schemas.DepartmentUpdate, db: Session = Depends(database.get_db)):
    dept = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found.")
    for key, value in dept_update.dict(exclude_unset=True).items():
        setattr(dept, key, value)
    db.commit()
    db.refresh(dept)
    return dept


# Feature: Delete a department
# DELETE /api/departments/{id}
# DB: DELETE from departments WHERE id = ?
@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(database.get_db)):
    dept = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found.")
    db.delete(dept)
    db.commit()
    return {"message": f"Department '{dept.name}' (ID: {department_id}) deleted."}
