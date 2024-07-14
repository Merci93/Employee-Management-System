-- Create databases
CREATE DATABASE employees;
CREATE DATABASE users;

-- Create default user.
\CONNECT users;

CREATE TABLE user (
    username VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    password VARCHAR(20),
);

INSERT INTO users (username, password)
VALUES ("admin@gmail.com", "admin", "admin", "ADmin1234");
