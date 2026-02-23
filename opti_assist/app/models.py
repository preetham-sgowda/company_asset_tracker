from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Department(Base):
    """
    Represents an organizational department within the company.
    Used for grouping employees and tracking cost centers.
    """
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Department Name (e.g., Engineering, HR)
    cost_center_code = Column(String(50))      # Unique code for financial tracking
    manager_employee_id = Column(Integer, nullable=True) # ID of the employee managing this department
    created_at = Column(DateTime, default=datetime.utcnow)

class Location(Base):
    """
    Represents a physical office or site location.
    Used to track where assets and employees are situated.
    """
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String(100), nullable=False) # Name of the site (e.g., Head Office, Warehouse A)
    address = Column(Text)
    city = Column(String(50))
    country = Column(String(50))
    is_active = Column(Boolean, default=True)

class Vendor(Base):
    """
    Represents a third-party vendor or supplier.
    Used for tracking asset procurement and maintenance services.
    """
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(150), nullable=False)
    contact_person = Column(String(100))
    contact_email = Column(String(150))
    support_phone = Column(String(50))
    website = Column(String(200))
    contract_expiry_date = Column(Date)

class AssetCategory(Base):
    """
    Represents a category for assets (e.g., Laptops, Furniture, Vehicles).
    Used for organization and defining default depreciation rules.
    """
    __tablename__ = "asset_categories"
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    parent_category_id = Column(Integer, nullable=True) # Allows for hierarchical categories
    depreciation_years = Column(Integer, default=3)    # Standard lifespan for assets in this category

class Employee(Base):
    """
    Represents a company employee.
    Employees can be assigned assets for their professional use.
    """
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False) # Unique company ID (e.g., EMP001)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(50))
    job_title = Column(String(100))
    department_id = Column(Integer, nullable=True) # Foreign key to departments
    location_id = Column(Integer, nullable=True)   # Foreign key to locations
    employment_status = Column(String(50), default='Active') # Active, Inactive, On Leave
    hire_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

class Asset(Base):
    """
    Represents a physical asset owned by the company.
    This is the core entity for tracking equipment, its status, and ownership.
    """
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(50), unique=True, nullable=False) # Unique barcode/RFID tag
    serial_number = Column(String(100))
    asset_name = Column(String(150), nullable=False)
    model_number = Column(String(100))
    category_id = Column(Integer, nullable=True) # Link to asset_categories
    status = Column(String(50), default='In Stock') # In Stock, Assigned, In Repair, Retired
    condition_grade = Column(String(20)) # New, Like New, Good, Fair, Poor
    vendor_id = Column(Integer, nullable=True) # Link to vendors
    purchase_date = Column(Date)
    purchase_cost = Column(Numeric(10, 2))
    warranty_expiry_date = Column(Date)
    order_number = Column(String(100))
    current_employee_id = Column(Integer, nullable=True) # Currently assigned employee
    current_location_id = Column(Integer, nullable=True) # Current physical location
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AssetAssignmentHistory(Base):
    """
    Tracks the movement of assets between employees over time.
    Provides an audit trail for asset stewardship.
    """
    __tablename__ = "asset_assignment_history"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    employee_id = Column(Integer, nullable=True)
    assigned_date = Column(DateTime, default=datetime.utcnow)
    returned_date = Column(DateTime, nullable=True) # NULL if currently assigned
    assigned_by_admin_id = Column(Integer, nullable=True)
    notes = Column(Text)

class MaintenanceLog(Base):
    """
    Records maintenance activities, repairs, and inspections for assets.
    Helps in calculating total cost of ownership (TCO) and asset health.
    """
    __tablename__ = "maintenance_logs"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    maintenance_type = Column(String(100)) # Preventive, Corrective, Inspection
    description = Column(Text)
    cost = Column(Numeric(10, 2))
    vendor_id = Column(Integer, nullable=True) # Link to vendor performing maintenance
    start_date = Column(Date)
    completion_date = Column(Date)
    status = Column(String(50)) # Pending, In Progress, Completed
