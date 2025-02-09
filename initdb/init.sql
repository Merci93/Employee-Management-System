-- INIT SQL
-- Create databases
CREATE DATABASE employees;

-- Create user table.
\connect employees

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    role CHAR(5),
    date_of_birth DATE,
    password VARCHAR(255) NOT NULL,
    employee_id INT NOT NULL
);

-- Add default admin
INSERT INTO users (first_name, last_name, email, role, date_of_birth, password, employee_id)
VALUES ('Admin', 'Admin', 'admin@gmail.com', 'Admin', '2024-01-01', 'ADmin1234', 1);


-- Create employee table 
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    salary INT NOT NULL,
    department_id INT NOT NULL,
    position_id INT NOT NULL,
    gender_id INT NOT NULL,
    date_of_birth DATE,
    hired_date DATE DEFAULT CURRENT_DATE
);

-- Add dummy employee data for tests
INSERT INTO employee (first_name, middle_name, last_name, email, phone, salary, department_id, position_id, gender_id, date_of_birth, hired_date)
VALUES ('Admin', 'Admin', 'Admin', 'admin@gmail.com', '070000', 34567, 1, 13, 1, '2005-05-19', '2024-12-05');


-- Create gender table
CREATE TABLE gender(
    id SERIAL PRIMARY KEY,
    gender VARCHAR(10)
);

-- Add data to gender table
INSERT INTO gender (gender)
VALUES ('Male'),
    ('Female');


-- Create departments table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Insert data into departments table
INSERT INTO departments (name)
VALUES ('IT'),
    ('Marketing'),
    ('Sales'),
    ('Research'),
    ('HR'),
    ('Data & Analytics');


-- Create positions table
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Insert data into roles table
INSERT INTO positions (name)
VALUES ('HR'),
    ('Data Engineer'),
    ('Solutions Architect'),
    ('Data Analyst'),
    ('Intern'),
    ('Business Analyst'),
    ('Senior Engineering Manager'),
    ('Data Scientist'),
    ('Web Developer'),
    ('Junior Data Engineer'),
    ('Cloud Architect'),
    ('Software Engineer'),
    ('Network Engineer'),
    ('DevOps Engineer'),
    ('Product Owner'),
    ('Senior Data Engineer'),
    ('Machine Learning Engineer');
