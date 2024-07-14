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
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO user (username, first_name, last_name, password, email) VALUES ("admin@gmail.com", "admin", "admin", "ADmin1234", "admin@gmail.com");


-- Create tables in the employee database and add data
