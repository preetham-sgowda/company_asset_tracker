from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel

# --- Shared Properties ---

class DepartmentBase(BaseModel):
    """Base schema for Department, containing shared fields."""
    name: str
    cost_center_code: Optional[str] = None
    manager_employee_id: Optional[int] = None

class LocationBase(BaseModel):
    """Base schema for Location, containing shared fields."""
    site_name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    is_active: bool = True

class VendorBase(BaseModel):
    """Base schema for Vendor, containing shared fields."""
    vendor_name: str
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    support_phone: Optional[str] = None
    website: Optional[str] = None
    contract_expiry_date: Optional[date] = None

class AssetCategoryBase(BaseModel):
    """Base schema for AssetCategory, containing shared fields."""
    category_name: str
    parent_category_id: Optional[int] = None
    depreciation_years: int = 3

class EmployeeBase(BaseModel):
    """Base schema for Employee, containing shared fields."""
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
    """Base schema for Asset, containing shared fields."""
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
    """Base schema for AssetAssignmentHistory, containing shared fields."""
    asset_id: int
    employee_id: Optional[int] = None
    assigned_date: Optional[datetime] = None
    returned_date: Optional[datetime] = None
    assigned_by_admin_id: Optional[int] = None
    notes: Optional[str] = None

class MaintenanceLogBase(BaseModel):
    """Base schema for MaintenanceLog, containing shared fields."""
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
    """Schema for creating a new Department."""
    pass

class LocationCreate(LocationBase):
    """Schema for creating a new Location."""
    pass

class VendorCreate(VendorBase):
    """Schema for creating a new Vendor."""
    pass

class AssetCategoryCreate(AssetCategoryBase):
    """Schema for creating a new AssetCategory."""
    pass

class EmployeeCreate(EmployeeBase):
    """Schema for creating a new Employee."""
    pass

class AssetCreate(AssetBase):
    """Schema for creating a new Asset."""
    pass

class AssetAssignmentHistoryCreate(AssetAssignmentHistoryBase):
    """Schema for creating a new Assignment History record."""
    pass

class MaintenanceLogCreate(MaintenanceLogBase):
    """Schema for creating a new Maintenance Log."""
    pass

# --- Update Models (all fields optional for PATCH) ---

class DepartmentUpdate(BaseModel):
    """Schema for updating an existing Department."""
    name: Optional[str] = None
    cost_center_code: Optional[str] = None
    manager_employee_id: Optional[int] = None

class LocationUpdate(BaseModel):
    """Schema for updating an existing Location."""
    site_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None

class VendorUpdate(BaseModel):
    """Schema for updating an existing Vendor."""
    vendor_name: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    support_phone: Optional[str] = None
    website: Optional[str] = None
    contract_expiry_date: Optional[date] = None

class AssetCategoryUpdate(BaseModel):
    """Schema for updating an existing AssetCategory."""
    category_name: Optional[str] = None
    parent_category_id: Optional[int] = None
    depreciation_years: Optional[int] = None

class EmployeeUpdate(BaseModel):
    """Schema for updating an existing Employee."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    job_title: Optional[str] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    employment_status: Optional[str] = None
    hire_date: Optional[date] = None

class AssetUpdate(BaseModel):
    """Schema for updating an existing Asset."""
    serial_number: Optional[str] = None
    asset_name: Optional[str] = None
    model_number: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None
    condition_grade: Optional[str] = None
    vendor_id: Optional[int] = None
    purchase_date: Optional[date] = None
    purchase_cost: Optional[float] = None
    warranty_expiry_date: Optional[date] = None
    order_number: Optional[str] = None
    current_employee_id: Optional[int] = None
    current_location_id: Optional[int] = None
    notes: Optional[str] = None

class MaintenanceLogUpdate(BaseModel):
    """Schema for updating an existing Maintenance Log."""
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    vendor_id: Optional[int] = None
    start_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: Optional[str] = None

# --- Special Request/Response Models ---

class AssignAssetRequest(BaseModel):
    """Schema for requesting an asset assignment."""
    asset_id: int
    employee_id: int
    assigned_by_admin_id: Optional[int] = None
    notes: Optional[str] = None

class ReturnAssetRequest(BaseModel):
    """Schema for requesting an asset return."""
    asset_id: int
    notes: Optional[str] = None

class EmployeeWithAssets(BaseModel):
    """Schema for Employee profile, including their currently assigned assets."""
    id: int
    employee_code: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    job_title: Optional[str] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    employment_status: str
    hire_date: Optional[date] = None
    created_at: datetime
    assigned_assets: List["Asset"] = []
    class Config:
        orm_mode = True

# --- Reading Models ---

class Department(DepartmentBase):
    """Complete schema for reading Department data."""
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Location(LocationBase):
    """Complete schema for reading Location data."""
    id: int
    class Config:
        orm_mode = True

class Vendor(VendorBase):
    """Complete schema for reading Vendor data."""
    id: int
    class Config:
        orm_mode = True

class AssetCategory(AssetCategoryBase):
    """Complete schema for reading AssetCategory data."""
    id: int
    class Config:
        orm_mode = True

class Employee(EmployeeBase):
    """Complete schema for reading Employee data."""
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Asset(AssetBase):
    """Complete schema for reading Asset data."""
    id: int
    created_at: datetime
    last_updated_at: datetime
    class Config:
        orm_mode = True

class AssetAssignmentHistory(AssetAssignmentHistoryBase):
    """Complete schema for reading AssetAssignmentHistory data."""
    id: int
    class Config:
        orm_mode = True

class MaintenanceLog(MaintenanceLogBase):
    """Complete schema for reading MaintenanceLog data."""
    id: int
    class Config:
        orm_mode = True

# Update forward references
EmployeeWithAssets.model_rebuild()
