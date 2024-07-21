-- INIT SQL
-- Create databases
CREATE DATABASE employees;
CREATE DATABASE users;

-- Create user table and add default user.
\connect users

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO users (username, first_name, last_name, email, password) VALUES ('admin@gmail.com', 'admin', 'admin', 'admin@gmail.com', 'ADmin1234');


-- Create tables in the employee database and add data
\connect employees

CREATE TABLE employees(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    salary INT NOT NULL,
)

CREATE  TABLE department(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
)
