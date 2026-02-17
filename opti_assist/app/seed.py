from datetime import date, datetime
from .database import SessionLocal, engine
from . import models

def seed_data():
    db = SessionLocal()
    
    # 1. Departments (Goal: 5+, Already has 6)
    # Adding a few more just in case
    new_depts = [
        models.Department(name="Quality Assurance", cost_center_code="CC-007"),
        models.Department(name="Legal & Compliance", cost_center_code="CC-008")
    ]
    
    # 2. Locations (Goal: 5+, Already has 4)
    new_locations = [
        models.Location(site_name="Berlin Office", city="Berlin", country="Germany"),
        models.Location(site_name="Tokyo Hub", city="Tokyo", country="Japan"),
        models.Location(site_name="San Francisco HQ", city="San Francisco", country="USA")
    ]
    
    # 3. Vendors (Goal: 5+, Already has 3)
    new_vendors = [
        models.Vendor(vendor_name="Lenovo Global", support_phone="1-800-LENOVO"),
        models.Vendor(vendor_name="Microsoft Stores", support_phone="1-800-MICROSOFT")
    ]
    
    # 4. Asset Categories (Goal: 5+, Already has 5)
    new_categories = [
        models.AssetCategory(category_name="Networking Gear", depreciation_years=5),
        models.AssetCategory(category_name="Office Furniture", depreciation_years=10)
    ]
    
    # 5. Employees (Goal: 5+, Already has 10)
    new_employees = [
        models.Employee(employee_code="EMP-1011", first_name="Wanda", last_name="Maximoff", email="wanda@company.com", department_id=3, location_id=1, job_title="Chaos Engineer"),
        models.Employee(employee_code="EMP-1012", first_name="Steve", last_name="Rogers", email="steve@company.com", department_id=1, location_id=1, job_title="Security Lead")
    ]
    
    # 6. Assets (Goal: 5+, Already has 5)
    new_assets = [
        models.Asset(asset_tag="AST-006", serial_number="SN-LEN-001", asset_name="Lenovo ThinkPad X1", category_id=1, status="In Stock", vendor_id=1, purchase_cost=1500.00, purchase_date=date(2024, 1, 1)),
        models.Asset(asset_tag="AST-007", serial_number="SN-CIS-001", asset_name="Cisco Router XR", category_id=1, status="In Repair", vendor_id=3, purchase_cost=2500.00, purchase_date=date(2023, 5, 12))
    ]
    
    # 7. Asset Assignment History (Goal: 5+, Already has 2)
    new_history = [
        models.AssetAssignmentHistory(asset_id=1, employee_id=9, assigned_date=datetime.now(), notes="Regular assignment"),
        models.AssetAssignmentHistory(asset_id=3, employee_id=1, assigned_date=datetime.now(), returned_date=datetime.now(), notes="Temporary loan"),
        models.AssetAssignmentHistory(asset_id=4, employee_id=7, assigned_date=datetime.now(), notes="Project replacement")
    ]
    
    # 8. Maintenance Logs (Goal: 5+, Already has 0)
    new_maintenance = [
        models.MaintenanceLog(asset_id=2, maintenance_type="Repair", description="Replace keyboard", cost=150.00, vendor_id=1, start_date=date(2024, 2, 1), completion_date=date(2024, 2, 5), status="Completed"),
        models.MaintenanceLog(asset_id=5, maintenance_type="Cleaning", description="Annual maintenance", cost=50.00, vendor_id=2, start_date=date(2024, 1, 10), completion_date=date(2024, 1, 10), status="Completed"),
        models.MaintenanceLog(asset_id=7, maintenance_type="Repair", description="Motherboard fix", cost=800.00, vendor_id=3, start_date=date(2024, 3, 1), status="In Progress"),
        models.MaintenanceLog(asset_id=1, maintenance_type="Upgrade", description="RAM upgrade", cost=200.00, vendor_id=2, start_date=date(2024, 2, 20), completion_date=date(2024, 2, 21), status="Completed"),
        models.MaintenanceLog(asset_id=4, maintenance_type="Screen Repair", description="Cracked screen replacement", cost=300.00, vendor_id=2, start_date=date(2024, 2, 25), status="Scheduled")
    ]

    try:
        db.add_all(new_depts)
        db.add_all(new_locations)
        db.add_all(new_vendors)
        db.add_all(new_categories)
        db.add_all(new_employees)
        db.add_all(new_assets)
        db.add_all(new_history)
        db.add_all(new_maintenance)
        
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
