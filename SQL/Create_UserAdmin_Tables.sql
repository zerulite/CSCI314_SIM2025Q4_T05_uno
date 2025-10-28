CREATE DATABASE IF NOT EXISTS csit314;
USE csit314;

CREATE TABLE UserProfile (
    profile VARCHAR(50) PRIMARY KEY,
    description VARCHAR(255)
);

CREATE TABLE UserAccount (
    userID VARCHAR(20) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    profile VARCHAR(50),
    userState ENUM('active', 'inactive') DEFAULT 'active',
    FOREIGN KEY (profile) REFERENCES UserProfile(profile)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);