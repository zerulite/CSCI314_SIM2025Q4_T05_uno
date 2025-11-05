CREATE TABLE Request (
    requestID INT PRIMARY KEY AUTO_INCREMENT,
    reqDescription VARCHAR(10000),
    reqCreatedOn DATETIME DEFAULT CURRENT_TIMESTAMP,
    helpNeededDate VARCHAR(10),
    helpNeededTime VARCHAR(10),
    reqStatus VARCHAR(20) DEFAULT 'Open',
    viewCount INT DEFAULT 0,
    shortlistCount INT DEFAULT 0,
    category VARCHAR(20),
    userID VARCHAR(20),
    FOREIGN KEY (category) REFERENCES Category(category),
    FOREIGN KEY (userID) REFERENCES UserAccount(userID)
);