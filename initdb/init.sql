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
    password VARCHAR(255) NOT NULL
);

-- Add default admin
INSERT INTO users (first_name, last_name, email, role, date_of_birth, password)
VALUES ('Admin', 'Admin', 'admin@gmail.com', 'admin', '2024-01-01', 'ADmin1234');


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
    role_id INT NOT NULL
);


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


-- Create roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL
);

-- Insert data into roles table
INSERT INTO roles (role)
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
