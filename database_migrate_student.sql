USE face_recognition;

-- Check the current schema before changing it:
-- SHOW COLUMNS FROM student;

-- Your error shows that the existing table uses Department, not Dep.
-- Run this only if Department already exists and the application previously
-- created a Dep column in another version:
-- ALTER TABLE student CHANGE COLUMN Dep Department VARCHAR(100) NOT NULL;

-- If Department already exists, no rename is needed. The application now uses
-- Department consistently.
ALTER TABLE student
    MODIFY COLUMN Department VARCHAR(100) NOT NULL;

-- Confirm the final column names:
SHOW COLUMNS FROM student;
