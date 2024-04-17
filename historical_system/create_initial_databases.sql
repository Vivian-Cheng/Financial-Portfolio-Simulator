CREATE DATABASE IF NOT EXISTS STOCK;
USE STOCK;

CREATE TABLE IF NOT EXISTS stocks (
    symbol  VARCHAR(6)      PRIMARY KEY,
    company VARCHAR(255)    NOT NULL    UNIQUE
);

CREATE TABLE IF NOT EXISTS stockhistory (
    symbol  VARCHAR(6)  NOT NULL,
    hdate   DATE        DEFAULT (CURRENT_DATE),
    o       FLOAT       NOT NULL, /* open */
    h       FLOAT       NOT NULL, /* high */
    l       FLOAT       NOT NULL, /* low */
    c       FLOAT       NOT NULL, /* close */
    volume  INT         NOT NULL,
    PRIMARY KEY (symbol, hdate),
    FOREIGN KEY (symbol)    REFERENCES stocks(symbol)
);


CREATE DATABASE IF NOT EXISTS SIMULATOR;
USE SIMULATOR;

CREATE TABLE IF NOT EXISTS users (
    id          INT             PRIMARY KEY AUTO_INCREMENT,
    username    VARCHAR(255)    NOT NULL    UNIQUE,
    passcode    VARCHAR(255)    NOT NULL,
    isAdmin     BOOLEAN         DEFAULT false
);

CREATE TABLE IF NOT EXISTS inventory (
    userId  INT         NOT NULL,
    symbol  VARCHAR(6)  NOT NULL,
    volume  INT         NOT NULL,
    PRIMARY KEY (userId, symbol),
    FOREIGN KEY (userId)    REFERENCES users(id),
    FOREIGN KEY (symbol)    REFERENCES STOCK.stocks(symbol)
);

CREATE TABLE IF NOT EXISTS transactions (
    id      INT         PRIMARY KEY AUTO_INCREMENT,
    buyerId INT         NOT NULL,
    symbol  VARCHAR(6)  NOT NULL,
    volume  INT         NOT NULL,
    txnTime TIMESTAMP   NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyerId)   REFERENCES users(id),
    FOREIGN KEY (symbol)    REFERENCES STOCK.stocks(symbol)
);
