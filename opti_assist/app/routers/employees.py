from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, database

router = APIRouter(prefix="/api/employees", tags=["Employees"])


# Feature: Register a new employee in the system
# POST /api/employees
# DB: INSERT into employees table
@router.post("/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    # Check for duplicate employee_code or email
    existing_code = db.query(models.Employee).filter(models.Employee.employee_code == employee.employee_code).first()
    if existing_code:
        raise HTTPException(status_code=400, detail=f"Employee with code '{employee.employee_code}' already exists.")
    existing_email = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail=f"Employee with email '{employee.email}' already exists.")
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


# Feature: View list of all active employees
# GET /api/employees?status=Active
# DB: SELECT * from employees [WHERE employment_status = ?]
@router.get("/", response_model=List[schemas.Employee])
def list_employees(
    status: Optional[str] = Query(None, description="Filter by employment status (e.g., 'Active', 'Inactive')"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Employee)
    if status:
        query = query.filter(models.Employee.employment_status == status)
    return query.offset(skip).limit(limit).all()


# Feature: View an employee's profile and their currently held assets
# GET /api/employees/{id}
# DB: SELECT * from employees WHERE id = ?; SELECT * from assets WHERE current_employee_id = ?
@router.get("/{employee_id}", response_model=schemas.EmployeeWithAssets)
def get_employee_with_assets(employee_id: int, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    assigned_assets = (
        db.query(models.Asset)
        .filter(models.Asset.current_employee_id == employee_id)
        .all()
    )
    # Build response manually
    emp_data = {
        "id": employee.id,
        "employee_code": employee.employee_code,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "phone_number": employee.phone_number,
        "job_title": employee.job_title,
        "department_id": employee.department_id,
        "location_id": employee.location_id,
        "employment_status": employee.employment_status,
        "hire_date": employee.hire_date,
        "created_at": employee.created_at,
        "assigned_assets": assigned_assets,
    }
    return emp_data


# Feature: Update employee details
# PATCH /api/employees/{id}
# DB: UPDATE employees SET ... WHERE id = ?
@router.patch("/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    update_data = employee_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee


# Feature: Deactivate an employee (Termination/Resignation)
# PATCH /api/employees/{id}/deactivate
# DB: UPDATE employees SET employment_status = 'Inactive' WHERE id = ?
@router.patch("/{employee_id}/deactivate", response_model=schemas.Employee)
def deactivate_employee(employee_id: int, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    employee.employment_status = "Inactive"
    db.commit()
    db.refresh(employee)
    return employee
