-- Run this script in MySQL Workbench or the mysql command line.
-- The application defaults to the corrected database name below.

CREATE DATABASE IF NOT EXISTS face_recognition
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE face_recognition;

CREATE TABLE IF NOT EXISTS register (
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100) NOT NULL DEFAULT '',
    contact VARCHAR(30) NOT NULL DEFAULT '',
    email VARCHAR(255) NOT NULL,
    secQ VARCHAR(255) NOT NULL,
    secA VARCHAR(255) NOT NULL DEFAULT '',
    `pass` VARCHAR(255) NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS student (
    Department VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL DEFAULT '',
    year VARCHAR(20) NOT NULL DEFAULT '',
    semester VARCHAR(20) NOT NULL DEFAULT '',
    Student_id VARCHAR(50) NOT NULL,
    Name VARCHAR(150) NOT NULL,
    Division VARCHAR(20) NOT NULL DEFAULT '',
    roll VARCHAR(50) NOT NULL DEFAULT '',
    Gender VARCHAR(20) NOT NULL DEFAULT '',
    dob VARCHAR(30) NOT NULL DEFAULT '',
    email VARCHAR(255) NOT NULL DEFAULT '',
    phone VARCHAR(30) NOT NULL DEFAULT '',
    address VARCHAR(255) NOT NULL DEFAULT '',
    teacher VARCHAR(150) NOT NULL DEFAULT '',
    photosample VARCHAR(20) NOT NULL DEFAULT '',
    PRIMARY KEY (Student_id)
);
