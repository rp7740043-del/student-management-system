-- ==============================================================================
-- College Student Management System (SMS) - Database Schema
-- Target Database: MySQL 8.0+ / MariaDB
-- Database Name: student_db
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- ------------------------------------------------------------------------------
-- Drop existing tables in reverse dependency order
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS marks;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS users;

-- ------------------------------------------------------------------------------
-- 1. Table: users (Authentication and Roles)
-- ------------------------------------------------------------------------------
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'ADMIN',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------------------------
-- 2. Table: students (Core Student Information)
-- ------------------------------------------------------------------------------
CREATE TABLE students (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    class_year VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    address TEXT,
    dob DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    admission_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------------------------
-- 3. Table: marks (Subject-wise Academic Performance)
-- ------------------------------------------------------------------------------
CREATE TABLE marks (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    marks_obtained DOUBLE NOT NULL,
    max_marks DOUBLE DEFAULT 100.0,
    CONSTRAINT fk_marks_student FOREIGN KEY (student_id) 
        REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------------------------
-- 4. Table: attendance (Class Attendance Records)
-- ------------------------------------------------------------------------------
CREATE TABLE attendance (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT NOT NULL,
    total_classes INT NOT NULL DEFAULT 0,
    attended_classes INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_attendance_student FOREIGN KEY (student_id) 
        REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==============================================================================
-- SAMPLE DATA INSERTION
-- Default credentials:
-- Admin: admin / admin123  (BCrypt hash: $2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi)
-- Teacher: teacher / teacher123 (BCrypt hash: $2a$10$wEeVq0aL5r7h2Wv5Z/7DTe6j1tOqg4aF8Q4U2X1y3w5Z7dTe6j1tO)
-- ==============================================================================

-- 1. Insert Users
INSERT INTO users (username, password, role) VALUES
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', 'ADMIN'),
('teacher', '$2a$10$wEeVq0aL5r7h2Wv5Z/7DTe6j1tOqg4aF8Q4U2X1y3w5Z7dTe6j1tO', 'TEACHER');

-- 2. Insert Students (12 Diverse Students)
INSERT INTO students (id, student_id, name, department, class_year, email, phone, address, dob, gender, admission_date) VALUES
(1, 'STU2024001', 'Aarav Sharma', 'CSE', 'TE', 'aarav.sharma@college.edu', '9876543210', '124 MG Road, Pune, Maharashtra', '2003-05-14', 'Male', '2022-08-01'),
(2, 'STU2024002', 'Priya Patel', 'IT', 'TE', 'priya.patel@college.edu', '9823456781', '45 Park Avenue, Mumbai, Maharashtra', '2003-08-22', 'Female', '2022-08-01'),
(3, 'STU2024003', 'Rohan Verma', 'AI&DS', 'SE', 'rohan.verma@college.edu', '9812345678', '78 Shivaji Nagar, Pune, Maharashtra', '2004-02-10', 'Male', '2023-08-10'),
(4, 'STU2024004', 'Ananya Deshmukh', 'ENTC', 'BE', 'ananya.d@college.edu', '9890123456', '12 Kothrud, Pune, Maharashtra', '2002-11-05', 'Female', '2021-08-15'),
(5, 'STU2024005', 'Vikramaditya Singh', 'Mechanical', 'TE', 'vikram.singh@college.edu', '9765432109', '56 Model Colony, Pune, Maharashtra', '2003-07-19', 'Male', '2022-08-01'),
(6, 'STU2024006', 'Sneha Kulkarni', 'CSE', 'FE', 'sneha.k@college.edu', '9845123478', '89 Baner Road, Pune, Maharashtra', '2005-03-30', 'Female', '2024-08-05'),
(7, 'STU2024007', 'Aditi Rao', 'Civil', 'SE', 'aditi.rao@college.edu', '9734567890', '23 Koregaon Park, Pune, Maharashtra', '2004-09-12', 'Female', '2023-08-10'),
(8, 'STU2024008', 'Rahul Joshi', 'IT', 'BE', 'rahul.joshi@college.edu', '9822334455', '67 Viman Nagar, Pune, Maharashtra', '2002-04-18', 'Male', '2021-08-15'),
(9, 'STU2024009', 'Tanvi Shinde', 'AI&DS', 'FE', 'tanvi.s@college.edu', '9811223344', '34 Aundh, Pune, Maharashtra', '2005-01-25', 'Female', '2024-08-05'),
(10, 'STU2024010', 'Siddharth Mehta', 'ENTC', 'TE', 'siddharth.m@college.edu', '9877889900', '101 FC Road, Pune, Maharashtra', '2003-12-08', 'Male', '2022-08-01'),
(11, 'STU2024011', 'Neha Gupta', 'Mechanical', 'BE', 'neha.gupta@college.edu', '9866554433', '15 Deccan Gymkhana, Pune, Maharashtra', '2002-06-15', 'Female', '2021-08-15'),
(12, 'STU2024012', 'Harsh Vardhan', 'Civil', 'FE', 'harsh.v@college.edu', '9855443322', '88 Hadapsar, Pune, Maharashtra', '2005-08-02', 'Male', '2024-08-05');

-- 3. Insert Marks for 5 subjects per student
INSERT INTO marks (student_id, subject, marks_obtained, max_marks) VALUES
(1, 'Object Oriented Programming', 88.0, 100.0),
(1, 'Database Management Systems', 92.0, 100.0),
(1, 'Data Structures & Algorithms', 85.0, 100.0),
(1, 'Computer Networks', 78.0, 100.0),
(1, 'Operating Systems', 84.0, 100.0),

(2, 'Object Oriented Programming', 95.0, 100.0),
(2, 'Database Management Systems', 94.0, 100.0),
(2, 'Data Structures & Algorithms', 91.0, 100.0),
(2, 'Computer Networks', 89.0, 100.0),
(2, 'Operating Systems', 93.0, 100.0),

(3, 'Object Oriented Programming', 72.0, 100.0),
(3, 'Database Management Systems', 68.0, 100.0),
(3, 'Data Structures & Algorithms', 75.0, 100.0),
(3, 'Computer Networks', 64.0, 100.0),
(3, 'Operating Systems', 70.0, 100.0),

(4, 'Object Oriented Programming', 81.0, 100.0),
(4, 'Database Management Systems', 85.0, 100.0),
(4, 'Data Structures & Algorithms', 79.0, 100.0),
(4, 'Computer Networks', 88.0, 100.0),
(4, 'Operating Systems', 82.0, 100.0),

(5, 'Object Oriented Programming', 62.0, 100.0),
(5, 'Database Management Systems', 58.0, 100.0),
(5, 'Data Structures & Algorithms', 65.0, 100.0),
(5, 'Computer Networks', 55.0, 100.0),
(5, 'Operating Systems', 60.0, 100.0),

(6, 'Object Oriented Programming', 78.0, 100.0),
(6, 'Database Management Systems', 80.0, 100.0),
(6, 'Data Structures & Algorithms', 82.0, 100.0),
(6, 'Computer Networks', 74.0, 100.0),
(6, 'Operating Systems', 76.0, 100.0),

(7, 'Object Oriented Programming', 55.0, 100.0),
(7, 'Database Management Systems', 62.0, 100.0),
(7, 'Data Structures & Algorithms', 58.0, 100.0),
(7, 'Computer Networks', 50.0, 100.0),
(7, 'Operating Systems', 54.0, 100.0),

(8, 'Object Oriented Programming', 45.0, 100.0),
(8, 'Database Management Systems', 48.0, 100.0),
(8, 'Data Structures & Algorithms', 32.0, 100.0),
(8, 'Computer Networks', 40.0, 100.0),
(8, 'Operating Systems', 42.0, 100.0),

(9, 'Object Oriented Programming', 89.0, 100.0),
(9, 'Database Management Systems', 91.0, 100.0),
(9, 'Data Structures & Algorithms', 87.0, 100.0),
(9, 'Computer Networks', 85.0, 100.0),
(9, 'Operating Systems', 90.0, 100.0),

(10, 'Object Oriented Programming', 74.0, 100.0),
(10, 'Database Management Systems', 70.0, 100.0),
(10, 'Data Structures & Algorithms', 72.0, 100.0),
(10, 'Computer Networks', 68.0, 100.0),
(10, 'Operating Systems', 75.0, 100.0),

(11, 'Object Oriented Programming', 65.0, 100.0),
(11, 'Database Management Systems', 70.0, 100.0),
(11, 'Data Structures & Algorithms', 68.0, 100.0),
(11, 'Computer Networks', 62.0, 100.0),
(11, 'Operating Systems', 66.0, 100.0),

(12, 'Object Oriented Programming', 38.0, 100.0),
(12, 'Database Management Systems', 42.0, 100.0),
(12, 'Data Structures & Algorithms', 40.0, 100.0),
(12, 'Computer Networks', 36.0, 100.0),
(12, 'Operating Systems', 41.0, 100.0);

-- 4. Insert Attendance records
INSERT INTO attendance (student_id, total_classes, attended_classes) VALUES
(1, 120, 108),
(2, 120, 114),
(3, 120, 85),
(4, 120, 102),
(5, 120, 92),
(6, 100, 88),
(7, 120, 80),
(8, 120, 72),
(9, 100, 94),
(10, 120, 100),
(11, 120, 110),
(12, 100, 70);
