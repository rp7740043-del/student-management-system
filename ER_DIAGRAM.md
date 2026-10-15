# Database Entity-Relationship (ER) Diagram Description

## 1. Overview & Architectural Design
The database for the **College Student Management System (SMS)** is named `student_db`. It utilizes the **InnoDB** storage engine to enforce ACID compliance, strict foreign key constraints, and referential integrity with cascading deletions (`ON DELETE CASCADE`).

```
+---------------------------------------------------------------------------------------------------+
|                                      DATABASE: student_db                                         |
+---------------------------------------------------------------------------------------------------+

            +-----------------------+
            |        USERS          |
            +-----------------------+
            | PK  id (BIGINT)       |
            |     username (VARCHAR)|
            |     password (VARCHAR)|
            |     role (VARCHAR)    |
            |     created_at        |
            +-----------------------+

                                  +---------------------------+
                                  |         STUDENTS          |
                                  +---------------------------+
                                  | PK   id (BIGINT)          |
                                  | UK   student_id (VARCHAR) |
                                  |      name (VARCHAR)       |
                                  |      department (VARCHAR) |
                                  |      class_year (VARCHAR) |
                                  | UK   email (VARCHAR)      |
                                  |      phone (VARCHAR)      |
                                  |      address (TEXT)       |
                                  |      dob (DATE)           |
                                  |      gender (VARCHAR)     |
                                  |      admission_date (DATE)|
                                  +---------------------------+
                                          |          |
                      1 : N (CASCADE)     |          |   1 : 1 (CASCADE)
                   +----------------------+          +----------------------+
                   |                                                        |
                   v                                                        v
      +-------------------------+                              +-------------------------+
      |          MARKS          |                              |       ATTENDANCE        |
      +-------------------------+                              +-------------------------+
      | PK  id (BIGINT)         |                              | PK  id (BIGINT)         |
      | FK  student_id (BIGINT) |                              | FK  student_id (BIGINT) |
      |     subject (VARCHAR)   |                              |     total_classes (INT) |
      |     marks_obtained (DBL)|                              |     attended_classes(INT|
      |     max_marks (DBL)     |                              +-------------------------+
      +-------------------------+
```

---

## 2. Table Specifications & Schema Definitions

### 2.1 Table: `users`
Maintains administrator and faculty credentials with BCrypt password hashing.
* `id` : `BIGINT AUTO_INCREMENT` &rarr; Primary Key.
* `username` : `VARCHAR(50) NOT NULL UNIQUE` &rarr; Unique administrative username.
* `password` : `VARCHAR(255) NOT NULL` &rarr; BCrypt salted password hash.
* `role` : `VARCHAR(20) NOT NULL DEFAULT 'ADMIN'` &rarr; Authorization role (`ADMIN`, `TEACHER`).
* `created_at` : `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`.

### 2.2 Table: `students`
Stores comprehensive academic and demographic records for each enrolled candidate.
* `id` : `BIGINT AUTO_INCREMENT` &rarr; Primary Key (internal surrogate identifier).
* `student_id` : `VARCHAR(30) NOT NULL UNIQUE` &rarr; University PRN / Roll number (e.g., `STU2024001`).
* `name` : `VARCHAR(100) NOT NULL` &rarr; Full student name.
* `department` : `VARCHAR(50) NOT NULL` &rarr; Department (`CSE`, `IT`, `AI&DS`, `ENTC`, `Mechanical`, `Civil`).
* `class_year` : `VARCHAR(20) NOT NULL` &rarr; Academic year (`FE`, `SE`, `TE`, `BE`).
* `email` : `VARCHAR(100) NOT NULL UNIQUE` &rarr; Validated email address.
* `phone` : `VARCHAR(15) NOT NULL` &rarr; 10-digit mobile number.
* `address` : `TEXT` &rarr; Residential address.
* `dob` : `DATE NOT NULL` &rarr; Date of birth.
* `gender` : `VARCHAR(10) NOT NULL` &rarr; Male / Female / Other.
* `admission_date` : `DATE NOT NULL` &rarr; Official enrollment date.
* `created_at` / `updated_at` : `TIMESTAMP`.

### 2.3 Table: `marks`
Stores subject-wise evaluation scores for the 5 curriculum subjects.
* `id` : `BIGINT AUTO_INCREMENT` &rarr; Primary Key.
* `student_id` : `BIGINT NOT NULL` &rarr; Foreign Key referencing `students(id)`.
* `subject` : `VARCHAR(100) NOT NULL` &rarr; Subject name (OOP, DBMS, DSA, CN, OS).
* `marks_obtained` : `DOUBLE NOT NULL` &rarr; Score achieved (0.0 - 100.0).
* `max_marks` : `DOUBLE DEFAULT 100.0` &rarr; Maximum subject mark.
* **Integrity Constraint:** `CONSTRAINT fk_marks_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE`.

### 2.4 Table: `attendance`
Stores cumulative class attendance and lecture delivery statistics.
* `id` : `BIGINT AUTO_INCREMENT` &rarr; Primary Key.
* `student_id` : `BIGINT NOT NULL` &rarr; Foreign Key referencing `students(id)`.
* `total_classes` : `INT NOT NULL DEFAULT 0` &rarr; Total lectures conducted.
* `attended_classes` : `INT NOT NULL DEFAULT 0` &rarr; Total lectures attended by candidate.
* **Integrity Constraint:** `CONSTRAINT fk_attendance_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE`.

---

## 3. Cardinality & Relationship Dynamics

1. **`students` to `marks` (One-to-Many - 1:N)**:
   - One student has records for multiple curriculum subjects (standard 5 core courses).
   - If a student record is removed, all corresponding subject marks are automatically purged via `ON DELETE CASCADE`.

2. **`students` to `attendance` (One-to-One - 1:1)**:
   - Each enrolled student possesses exactly one cumulative attendance tracking record.
   - Deleting a student cascades and deletes their attendance record cleanly.
