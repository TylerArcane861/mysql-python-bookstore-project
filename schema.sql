CREATE DATABASE IF NOT EXISTS project2;
USE project2;

CREATE TABLE IF NOT EXISTS publishers (
    pubID INT NOT NULL,
    pname VARCHAR(30),
    email VARCHAR(50),
    phone VARCHAR(30),
    PRIMARY KEY (pubID),
    UNIQUE INDEX email_UNIQUE (email ASC)
);

CREATE TABLE IF NOT EXISTS subjects (
    subID VARCHAR(5) NOT NULL,
    sName VARCHAR(30),
    PRIMARY KEY (subID)
);

CREATE TABLE IF NOT EXISTS authors (
    auID INT NOT NULL,
    aName VARCHAR(30),
    email VARCHAR(50),
    phone VARCHAR(30),
    PRIMARY KEY (auID),
    UNIQUE INDEX email_UNIQUE (email ASC)
);

CREATE TABLE IF NOT EXISTS titles (
    titleID INT NOT NULL,
    title VARCHAR(30),
    pubID INT,
    subID VARCHAR(5),
    pubDate DATE,
    cover VARCHAR(10),
    price INT,
    PRIMARY KEY (titleID),
    FOREIGN KEY (pubID) REFERENCES publishers(pubID),
    FOREIGN KEY (subID) REFERENCES subjects(subID)
);

CREATE TABLE IF NOT EXISTS titleauthors (
    titleID INT NOT NULL,
    auID INT NOT NULL,
    importance INT,
    PRIMARY KEY (titleID, auID),
    FOREIGN KEY (titleID) REFERENCES titles(titleID),
    FOREIGN KEY (auID) REFERENCES authors(auID)
);