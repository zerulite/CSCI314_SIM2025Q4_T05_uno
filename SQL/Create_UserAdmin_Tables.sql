CREATE DATABASE IF NOT EXISTS csit314;
USE csit314;

CREATE TABLE UserProfile (
    UserType VARCHAR(50) PRIMARY KEY,
    Description VARCHAR(255)
);

CREATE TABLE UserAccount (
    UserID VARCHAR(20) PRIMARY KEY,
    Password VARCHAR(255) NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    UserType VARCHAR(50),
    UserState ENUM('active', 'inactive') DEFAULT 'active',
    FOREIGN KEY (UserType) REFERENCES UserProfile(UserType)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);