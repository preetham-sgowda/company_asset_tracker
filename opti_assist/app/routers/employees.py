from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, database

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.post("/", response_model=schemas.Employee, status_code=201)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    """
    Register a new employee in the asset management system.
    
    - **employee_code**: Unique corporate ID.
    - **email**: Must be unique.
    """
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


@router.get("/", response_model=List[schemas.Employee])
def list_employees(
    status: Optional[str] = Query(None, description="Filter by employment status (e.g., 'Active', 'Inactive')"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """
    List all employees with optional status filtering and pagination.
    """
    query = db.query(models.Employee)
    if status:
        query = query.filter(models.Employee.employment_status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{employee_id}", response_model=schemas.EmployeeWithAssets)
def get_employee_with_assets(employee_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve an employee's profile including a list of all assets currently assigned to them.
    """
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    assigned_assets = (
        db.query(models.Asset)
        .filter(models.Asset.current_employee_id == employee_id)
        .all()
    )
    
    # Build response manually to include the relationship-like data
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


@router.patch("/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(database.get_db)):
    """
    Update details for an existing employee.
    """
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    update_data = employee_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
    
    db.commit()
    db.refresh(employee)
    return employee


@router.patch("/{employee_id}/deactivate", response_model=schemas.Employee)
def deactivate_employee(employee_id: int, db: Session = Depends(database.get_db)):
    """
    Deactivate an employee (e.g., in case of termination or resignation).
    Sets employment status to 'Inactive'.
    """
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    employee.employment_status = "Inactive"
    db.commit()
    db.refresh(employee)
    return employee
