-- PostgreSQL Database Dump
-- Project: Enterprise Asset Management System (Industrial Grade)
-- Scale: 1000+ Employees, HR Integration, Audit Trails
-- Constraint: No Foreign Key Constraints (Soft Linking only)

-- Database creation is handled by Docker POSTGRES_DB environment variable
-- CREATE DATABASE asset_db;

-- ---------------------------------------------------------
-- 1. REFERENCE TABLES (Categories, Locations, Vendors, Departments)
-- ---------------------------------------------------------

-- 1.1 Departments (Mirrors HR Structure)
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cost_center_code VARCHAR(50), -- Useful for Finance/HR
    manager_employee_id INT, -- Soft link to employees.id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1.2 Locations (Physical places where assets live)
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    site_name VARCHAR(100) NOT NULL, -- e.g., "HQ - Building A", "Remote"
    address TEXT,
    city VARCHAR(50),
    country VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

-- 1.3 Vendors (Procurement sources)
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    contact_email VARCHAR(150),
    support_phone VARCHAR(50),
    website VARCHAR(200),
    contract_expiry_date DATE
);

-- 1.4 Asset Categories (Taxonomy)
CREATE TABLE asset_categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL, -- e.g., "Laptop", "Furniture"
    parent_category_id INT, -- Soft link for hierarchy (e.g., Hardware -> Laptop)
    depreciation_years INT DEFAULT 3 -- For Finance usage
);

-- ---------------------------------------------------------
-- 2. CORE ENTITIES (Employees, Assets)
-- ---------------------------------------------------------

-- 2.1 Employees (The "1000 Users")
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) NOT NULL UNIQUE, -- The HR ID (e.g., EMP-1092)
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone_number VARCHAR(50),
    job_title VARCHAR(100),
    department_id INT, -- Soft link to departments.id
    location_id INT, -- Soft link to locations.id (Home base)
    employment_status VARCHAR(50) DEFAULT 'Active', -- Active, Terminated, On Leave
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2.2 Assets ( The Main Inventory)
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    -- Identification
    asset_tag VARCHAR(50) NOT NULL UNIQUE, -- Internal Sticker ID
    serial_number VARCHAR(100), -- Manufacturer Serial
    asset_name VARCHAR(150) NOT NULL,
    model_number VARCHAR(100),
    
    -- Classification
    category_id INT, -- Soft link to asset_categories.id
    status VARCHAR(50) DEFAULT 'In Stock', -- In Stock, Assigned, In Repair, Retired, Lost
    condition_grade VARCHAR(20), -- New, Good, Fair, Poor
    
    -- Financials & Procurement
    vendor_id INT, -- Soft link to vendors.id
    purchase_date DATE,
    purchase_cost DECIMAL(10, 2),
    warranty_expiry_date DATE,
    order_number VARCHAR(100),
    
    -- Current Assignment (The "Right Now" view)
    current_employee_id INT, -- Soft link to employees.id (NULL if unassigned)
    current_location_id INT, -- Soft link to locations.id
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------
-- 3. LOGGING & LIFECYCLE (History, Maintenance)
-- ---------------------------------------------------------

-- 3.1 Asset Assignment History (The "Audit Trail")
-- CRITICAL: This table answers "Who had this laptop 6 months ago?"
CREATE TABLE asset_assignment_history (
    id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL, -- Soft link to assets.id
    employee_id INT, -- Soft link to employees.id
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    returned_date TIMESTAMP,
    assigned_by_admin_id INT, -- Who performed the action
    notes TEXT -- e.g., "Given for temporary project"
);

-- 3.2 Maintenance Logs (Repairs & Upgrades)
CREATE TABLE maintenance_logs (
    id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL, -- Soft link to assets.id
    maintenance_type VARCHAR(100), -- Repair, Upgrade, Cleaning
    description TEXT,
    cost DECIMAL(10, 2),
    vendor_id INT, -- Soft link to vendors.id (Who fixed it)
    start_date DATE,
    completion_date DATE,
    status VARCHAR(50) -- Scheduled, In Progress, Completed
);

-- ---------------------------------------------------------
-- 4. DUMMY DATA INSERTION (For Testing)
-- ---------------------------------------------------------

-- 4.1 Setup Departments
INSERT INTO departments (name, cost_center_code) VALUES 
('Executive Leadership', 'CC-001'),
('Human Resources', 'CC-002'),
('Engineering - Backend', 'CC-003'),
('Engineering - Frontend', 'CC-004'),
('Sales', 'CC-005'),
('IT Support', 'CC-006');

-- 4.2 Setup Locations
INSERT INTO locations (site_name, city, country) VALUES 
('HQ - Building A', 'New York', 'USA'),
('Warehouse - East', 'Jersey City', 'USA'),
('Remote - USA', 'N/A', 'USA'),
('London Branch', 'London', 'UK');

-- 4.3 Setup Categories
INSERT INTO asset_categories (category_name, depreciation_years) VALUES 
('Laptop - Windows', 3),
('Laptop - Mac', 3),
('Monitor', 5),
('Mobile Phone', 2),
('Software License', 1);

-- 4.4 Setup Vendors
INSERT INTO vendors (vendor_name, support_phone) VALUES 
('Dell Enterprise', '1-800-DELL'),
('Apple Business', '1-800-APPLE'),
('CDW Corp', '1-800-CDW');

-- 4.5 Create Employees (Sample 10)
INSERT INTO employees (employee_code, first_name, last_name, email, department_id, location_id, job_title) VALUES 
('EMP-1001', 'John', 'Doe', 'john.doe@company.com', 6, 1, 'IT Administrator'),
('EMP-1002', 'Sarah', 'Connor', 'sarah.c@company.com', 2, 1, 'HR Manager'),
('EMP-1003', 'Michael', 'Scott', 'm.scott@company.com', 5, 1, 'Regional Manager'),
('EMP-1004', 'Neo', 'Anderson', 'neo@company.com', 3, 3, 'Senior Backend Dev'),
('EMP-1005', 'Trinity', 'Moss', 'trinity@company.com', 3, 3, 'DevOps Engineer'),
('EMP-1006', 'Bruce', 'Wayne', 'bruce@company.com', 1, 1, 'CEO'),
('EMP-1007', 'Clark', 'Kent', 'clark@company.com', 5, 2, 'Field Sales'),
('EMP-1008', 'Diana', 'Prince', 'diana@company.com', 2, 4, 'Recruiter'),
('EMP-1009', 'Tony', 'Stark', 'tony@company.com', 3, 1, 'CTO'),
('EMP-1010', 'Peter', 'Parker', 'peter@company.com', 4, 1, 'Intern Developer');

-- 4.6 Create Assets
INSERT INTO assets (asset_tag, serial_number, asset_name, category_id, status, vendor_id, purchase_cost, purchase_date, current_employee_id) VALUES 
('AST-001', 'SN-MAC-9988', 'MacBook Pro M3 Max', 2, 'Assigned', 2, 3500.00, '2024-01-15', 9), -- Tony Stark
('AST-002', 'SN-DELL-1122', 'Dell Latitude 7400', 1, 'Assigned', 1, 1200.00, '2023-06-10', 3), -- Michael Scott
('AST-003', 'SN-MON-5544', 'Dell Ultrasharp 27', 3, 'In Stock', 3, 400.00, '2023-08-01', NULL),
('AST-004', 'SN-PHN-3322', 'iPhone 15', 4, 'Assigned', 2, 999.00, '2024-02-01', 7), -- Clark Kent
('AST-005', 'SN-MAC-7766', 'MacBook Air M2', 2, 'Assigned', 2, 1100.00, '2023-11-20', 8); -- Diana

-- 4.7 Create History Logs (Simulating previous actions)
-- Note: This is crucial for "Industrial" grade to show chain of custody
INSERT INTO asset_assignment_history (asset_id, employee_id, assigned_date, returned_date, notes) VALUES 
(2, 1, '2023-06-11', '2023-06-15', 'Initial setup by IT'),
(2, 3, '2023-06-16', NULL, 'Assigned to Michael Scott');