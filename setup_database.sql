CREATE DATABASE IF NOT EXISTS Student_info;
USE Student_info;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Student_name VARCHAR(100) NOT NULL,
    Student_id VARCHAR(20) UNIQUE NOT NULL,
    Department VARCHAR(50) NOT NULL,
    Study_year INT NOT NULL,
    Semester INT NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Hashed_pass VARCHAR(255) NOT NULL,
    Face_encoded LONGBLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Function to determine time slot based on current time
DELIMITER //
CREATE FUNCTION get_time_slot() 
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE current_time TIME;
    SET current_time = CURRENT_TIME();
    
    RETURN CASE
        WHEN current_time BETWEEN '08:00:00' AND '09:00:00' THEN '8:00-9:00'
        WHEN current_time BETWEEN '09:00:00' AND '10:00:00' THEN '9:00-10:00'
        WHEN current_time BETWEEN '10:00:00' AND '11:00:00' THEN '10:00-11:00'
        WHEN current_time BETWEEN '11:00:00' AND '12:00:00' THEN '11:00-12:00'
        WHEN current_time BETWEEN '12:00:00' AND '13:00:00' THEN '12:00-13:00'
        WHEN current_time BETWEEN '14:00:00' AND '15:00:00' THEN '14:00-15:00'
        WHEN current_time BETWEEN '15:00:00' AND '16:00:00' THEN '15:00-16:00'
        WHEN current_time BETWEEN '16:00:00' AND '17:00:00' THEN '16:00-17:00'
        ELSE 'Invalid Time'
    END;
END //
DELIMITER ;


-- Create tables for IT department (Semesters 1-8)
CREATE TABLE IF NOT EXISTS attendance_IT_1 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_IT_2 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_IT_3 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_IT_4 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_IT_5 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_IT_6 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_IT_7 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_IT_8 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

-- Create tables for CSE department (Semesters 1-8)
CREATE TABLE IF NOT EXISTS attendance_CSE_1 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CSE_2 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CSE_3 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CSE_4 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CSE_5 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CSE_6 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CSE_7 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CSE_8 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

-- Create tables for AI&DS department (Semesters 1-8)
CREATE TABLE IF NOT EXISTS attendance_AI_DS_1 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_AI_DS_2 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_AI_DS_3 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_AI_DS_4 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_AI_DS_5 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_AI_DS_6 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_AI_DS_7 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_AI_DS_8 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

-- Create tables for CME department (Semesters 1-8)
CREATE TABLE IF NOT EXISTS attendance_CME_1 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CME_2 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CME_3 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CME_4 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CME_5 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CME_6 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CME_7 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_CME_8 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

-- Create tables for ECE department (Semesters 1-8)
CREATE TABLE IF NOT EXISTS attendance_ECE_1 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_ECE_2 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_ECE_3 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_ECE_4 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_ECE_5 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_ECE_6 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_ECE_7 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_ECE_8 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

-- Create tables for EEE department (Semesters 1-8)
CREATE TABLE IF NOT EXISTS attendance_EEE_1 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_EEE_2 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_EEE_3 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_EEE_4 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_EEE_5 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_EEE_6 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_EEE_7 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
);

CREATE TABLE IF NOT EXISTS attendance_EEE_8 (
    Date DATE NOT NULL,
    Student_id VARCHAR(100) NOT NULL,
    Subject VARCHAR(100) NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (Date, Student_id, Subject, Time_slot)
); 