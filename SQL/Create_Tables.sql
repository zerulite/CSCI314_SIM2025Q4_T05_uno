CREATE DATABASE IF NOT EXISTS csit314;
USE csit314;

CREATE TABLE IF NOT EXISTS UserProfile (
    profile VARCHAR(50) PRIMARY KEY,
    description VARCHAR(255),
    profileState VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS UserAccount (
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

CREATE TABLE IF NOT EXISTS Category (
    category VARCHAR(20) PRIMARY KEY,
    description VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Request (
    requestID INT PRIMARY KEY AUTO_INCREMENT,
    reqDescription VARCHAR(10000),
    helpNeededDate DATE,
    helpNeededTime TIME,
    reqStatus VARCHAR(20) DEFAULT 'Open',
    viewCount INT DEFAULT 0,
    shortlistCount INT DEFAULT 0,
    category VARCHAR(20),
    userID VARCHAR(20),
    volunteer VARCHAR(30) NULL,
    FOREIGN KEY (category) REFERENCES Category(category),
    FOREIGN KEY (userID) REFERENCES UserAccount(userID)
);

CREATE TABLE IF NOT EXISTS RequestShortlist (
    requestID INT,
    userID VARCHAR(20),
    PRIMARY KEY (requestID, userID),
    FOREIGN KEY (requestID) REFERENCES Request(requestID),
    FOREIGN KEY (userID) REFERENCES UserAccount(userID)
);