from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel

# --- Shared Properties ---
class DepartmentBase(BaseModel):
    name: str
    cost_center_code: Optional[str] = None
    manager_employee_id: Optional[int] = None

class LocationBase(BaseModel):
    site_name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    is_active: bool = True

class VendorBase(BaseModel):
    vendor_name: str
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    support_phone: Optional[str] = None
    website: Optional[str] = None
    contract_expiry_date: Optional[date] = None

class AssetCategoryBase(BaseModel):
    category_name: str
    parent_category_id: Optional[int] = None
    depreciation_years: int = 3

class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    job_title: Optional[str] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    employment_status: str = 'Active'
    hire_date: Optional[date] = None

class AssetBase(BaseModel):
    asset_tag: str
    serial_number: Optional[str] = None
    asset_name: str
    model_number: Optional[str] = None
    category_id: Optional[int] = None
    status: str = 'In Stock'
    condition_grade: Optional[str] = None
    vendor_id: Optional[int] = None
    purchase_date: Optional[date] = None
    purchase_cost: Optional[float] = None
    warranty_expiry_date: Optional[date] = None
    order_number: Optional[str] = None
    current_employee_id: Optional[int] = None
    current_location_id: Optional[int] = None
    notes: Optional[str] = None

class AssetAssignmentHistoryBase(BaseModel):
    asset_id: int
    employee_id: Optional[int] = None
    assigned_date: Optional[datetime] = None
    returned_date: Optional[datetime] = None
    assigned_by_admin_id: Optional[int] = None
    notes: Optional[str] = None

class MaintenanceLogBase(BaseModel):
    asset_id: int
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    vendor_id: Optional[int] = None
    start_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: Optional[str] = None

# --- Creation Models ---
class DepartmentCreate(DepartmentBase):
    pass

class LocationCreate(LocationBase):
    pass

class VendorCreate(VendorBase):
    pass

class AssetCategoryCreate(AssetCategoryBase):
    pass

class EmployeeCreate(EmployeeBase):
    pass

class AssetCreate(AssetBase):
    pass

class AssetAssignmentHistoryCreate(AssetAssignmentHistoryBase):
    pass

class MaintenanceLogCreate(MaintenanceLogBase):
    pass

# --- Reading Models ---
class Department(DepartmentBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Location(LocationBase):
    id: int
    class Config:
        orm_mode = True

class Vendor(VendorBase):
    id: int
    class Config:
        orm_mode = True

class AssetCategory(AssetCategoryBase):
    id: int
    class Config:
        orm_mode = True

class Employee(EmployeeBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Asset(AssetBase):
    id: int
    created_at: datetime
    last_updated_at: datetime
    class Config:
        orm_mode = True

class AssetAssignmentHistory(AssetAssignmentHistoryBase):
    id: int
    class Config:
        orm_mode = True

class MaintenanceLog(MaintenanceLogBase):
    id: int
    class Config:
        orm_mode = True
