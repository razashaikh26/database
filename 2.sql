-- Drop existing tables if they exist
DROP TABLE IF EXISTS billing;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS artificial_teeth_sizes;
DROP TABLE IF EXISTS artificial_teeth;
DROP TABLE IF EXISTS dental_services;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS dentists;
DROP TABLE IF EXISTS equipment;

-- Create database
DROP DATABASE IF EXISTS dental_clinic;
CREATE DATABASE dental_clinic;
USE dental_clinic;

-- Create patients table
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT,
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    medical_history TEXT,
    allergies TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    insurance_provider VARCHAR(100),
    insurance_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create dentists table
CREATE TABLE dentists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    experience_years INT,
    description TEXT,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    availability TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create dental services table
CREATE TABLE dental_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    duration_minutes INT,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create artificial teeth table
CREATE TABLE artificial_teeth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    size VARCHAR(50) NOT NULL,
    material VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    warranty_months INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create artificial teeth sizes table
CREATE TABLE artificial_teeth_sizes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    size_name VARCHAR(50) NOT NULL,
    dimensions VARCHAR(100) NOT NULL,
    material VARCHAR(100) NOT NULL,
    base_price DECIMAL(10,2) NOT NULL,
    additional_features TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create appointments table
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    dentist_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (dentist_id) REFERENCES dentists(id)
);

-- Create equipment table
CREATE TABLE equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    purpose VARCHAR(200),
    purchase_date DATE,
    last_maintenance DATE,
    next_maintenance DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create billing table
CREATE TABLE billing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    teeth_size_id INT,
    base_amount DECIMAL(10,2) NOT NULL,
    additional_charges DECIMAL(10,2) DEFAULT 0.00,
    discount DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_status ENUM('Pending', 'Paid', 'Partially Paid') DEFAULT 'Pending',
    payment_method VARCHAR(50),
    billing_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (teeth_size_id) REFERENCES artificial_teeth_sizes(id)
);

-- Insert sample data for patients
INSERT INTO patients (name, email, phone, address, date_of_birth, gender, medical_history) VALUES
('John Doe', 'john.doe@email.com', '555-0101', '123 Main St, City', '1985-06-15', 'Male', 'No major issues'),
('Jane Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave, City', '1990-03-22', 'Female', 'Diabetes Type 2'),
('Mike Johnson', 'mike.j@email.com', '555-0103', '789 Pine Rd, City', '1978-11-30', 'Male', 'High blood pressure');

-- Insert sample data for dentists
INSERT INTO dentists (name, specialization, experience_years, description) VALUES
('Dr. John Smith', 'General Dentistry', 15, 'Specialized in preventive care'),
('Dr. Sarah Johnson', 'Orthodontics', 10, 'Expert in braces and alignments'),
('Dr. Michael Brown', 'Prosthodontics', 12, 'Specialized in artificial teeth');

-- Insert sample data for dental services
INSERT INTO dental_services (service_name, description, duration_minutes, price) VALUES
('General Checkup', 'Complete dental examination', 30, 100.00),
('Root Canal', 'Root canal treatment', 90, 800.00),
('Teeth Whitening', 'Professional whitening', 60, 300.00),
('Dental Crown', 'Crown installation', 120, 1000.00);

-- Insert sample data for artificial teeth sizes
INSERT INTO artificial_teeth_sizes (size_name, dimensions, material, base_price, additional_features) VALUES
('Small', '28mm x 14mm', 'Porcelain', 500.00, 'Standard finish'),
('Medium', '32mm x 16mm', 'Porcelain', 600.00, 'Standard finish'),
('Large', '36mm x 18mm', 'Porcelain', 700.00, 'Standard finish'),
('Premium Small', '28mm x 14mm', 'Zirconia', 800.00, 'Premium finish'),
('Premium Medium', '32mm x 16mm', 'Zirconia', 900.00, 'Premium finish'),
('Premium Large', '36mm x 18mm', 'Zirconia', 1000.00, 'Premium finish');

-- Insert sample data for equipment
INSERT INTO equipment (name, description, purpose, purchase_date) VALUES
('Digital X-Ray', 'Modern imaging system', 'Dental imaging', '2023-01-15'),
('Dental Chair', 'Advanced dental chair', 'Patient comfort', '2023-01-15'),
('Sterilization Unit', 'Autoclave system', 'Equipment sterilization', '2023-01-15');