# College Student Management System (ERP Portal)
### Object-Oriented Programming (OOP) Mini Project in Java & Spring Boot
http://localhost:8082/login
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.5-brightgreen.svg)
![Java](https://img.shields.io/badge/Java-17%20LTS-orange.svg)
![Database](https://img.shields.io/badge/Database-MySQL%208.0-blue.svg)
![Frontend](https://img.shields.io/badge/Frontend-Thymeleaf%20%2B%20Bootstrap%205-purple.svg)
![License](https://img.shields.io/badge/License-Academic%20Use-lightgrey.svg)

A complete, production-grade **College Student Management System** built with **Java 17, Spring Boot, Spring Data JPA, MySQL, Thymeleaf, and Bootstrap 5**. The portal is designed as an enterprise-grade University ERP for student admissions, academic marks entry, live attendance tracking with statutory shortage alerts, and official grade transcript generation with print/PDF support.

---

## 1. OOP Concepts Mapping (Viva Examination Guide)

Every fundamental Object-Oriented Programming paradigm is explicitly implemented, documented, and commented throughout the codebase:

| OOP Concept | Implementation Location in Project | Viva Explanation & Code Demonstration |
| :--- | :--- | :--- |
| **Encapsulation** | [Person.java](src/main/java/com/college/sms/model/Person.java)<br>[Student.java](src/main/java/com/college/sms/model/Student.java)<br>[Mark.java](src/main/java/com/college/sms/model/Mark.java)<br>[Attendance.java](src/main/java/com/college/sms/model/Attendance.java)<br>[User.java](src/main/java/com/college/sms/model/User.java) | All class data attributes are declared `private`. Internal state cannot be modified directly from outside. Access is guarded through `public` getters and validated setters (e.g., `Mark.setMarksObtained()` enforces bounds $0.0 \le \text{marks} \le 100.0$ and throws `InvalidMarksException`). |
| **Inheritance** | [Person.java](src/main/java/com/college/sms/model/Person.java) &rarr;<br>[Student.java](src/main/java/com/college/sms/model/Student.java) | `Student` extends abstract `Person`. Common identity, biographical, and contact fields (`id`, `name`, `email`, `phone`, `dob`, `gender`, `address`) are defined once in `Person` and inherited by `Student`. Code reusability is maximized. |
| **Abstraction** | [Reportable.java](src/main/java/com/college/sms/model/Reportable.java)<br>[StudentOperations.java](src/main/java/com/college/sms/model/StudentOperations.java)<br>[StudentService.java](src/main/java/com/college/sms/service/StudentService.java) | High-level contracts define *what* behaviors are required without exposing *how* they are executed. The `Reportable` interface specifies `calculatePercentage()`, `determineGrade()`, and `getResultStatus()`. Controllers depend strictly on service abstractions rather than concrete DAO implementations. |
| **Polymorphism: Method Overriding** | [Student.java](src/main/java/com/college/sms/model/Student.java) | **Runtime Polymorphism:** `Student` provides child-specific overrides of `Person.displayDetails()` and `Person.getRoleDescription()`, as well as fulfilling the `Reportable` contract. Calls resolved dynamically at runtime. |
| **Polymorphism: Method Overloading** | [StudentService.java](src/main/java/com/college/sms/service/StudentService.java)<br>[StudentServiceImpl.java](src/main/java/com/college/sms/service/impl/StudentServiceImpl.java) | **Compile-Time Polymorphism:** The method `searchStudent()` is overloaded with distinct parameter signatures:<br>1. `searchStudent(Long id)` &ndash; search by numeric internal ID<br>2. `searchStudent(int id)` &ndash; search by integer roll number<br>3. `searchStudent(String query)` &ndash; search by student roll code or name partial match<br>4. `searchStudent(String name, String department)` &ndash; search with department filter |
| **Constructors & `super` / `this`** | [Student.java](src/main/java/com/college/sms/model/Student.java) | The parameterized constructor calls `super(id, name, email, phone, address, dob, gender)` to delegate initialization to the parent `Person` constructor, and uses `this.studentId = studentId` to disambiguate instance variables from arguments. |
| **Static Members** | [AppConstants.java](src/main/java/com/college/sms/util/AppConstants.java)<br>[GradeCalculator.java](src/main/java/com/college/sms/util/GradeCalculator.java)<br>[Student.java](src/main/java/com/college/sms/model/Student.java) | `AppConstants` defines `static final` constants (`COLLEGE_NAME`, `DEFAULT_SUBJECTS`). `GradeCalculator` provides stateless `static` methods for letter grade determination. `Student` maintains a `static int totalStudentsInstantiated` instance counter. |
| **Custom Exception Handling** | [StudentNotFoundException.java](src/main/java/com/college/sms/exception/StudentNotFoundException.java)<br>[InvalidMarksException.java](src/main/java/com/college/sms/exception/InvalidMarksException.java)<br>[DuplicateStudentException.java](src/main/java/com/college/sms/exception/DuplicateStudentException.java)<br>[GlobalExceptionHandler.java](src/main/java/com/college/sms/exception/GlobalExceptionHandler.java) | Custom checked/unchecked exceptions represent domain boundary violations. `GlobalExceptionHandler` with `@ControllerAdvice` centrally intercepts errors and renders user-friendly error views or toast flash notices. |
| **Collections Framework** | [StudentServiceImpl.java](src/main/java/com/college/sms/service/impl/StudentServiceImpl.java)<br>[ReportServiceImpl.java](src/main/java/com/college/sms/service/impl/ReportServiceImpl.java) | `List<Student>`, `List<Mark>`, `Map<String, Long>` (department counts for charts), `Map<String, Double>` (subject-wise average marks), and `Set` collections are utilized for in-memory operations and analytic aggregation. |
| **Layered Architecture** | `model` &rarr; `repository` &rarr; `service` &rarr; `controller` &rarr; `view` | Separation of Concerns (SoC) ensures code modularity, testability, and clean decoupling across 8 dedicated packages. |

---

## 2. Default Access Credentials

The portal is protected with session authentication and BCrypt password encryption:

| User Role | Username | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full access: CRUD, Marks, Attendance, Reports, System Configuration |
| **Faculty / Teacher** | `teacher` | `teacher123` | Student viewing, marks recording, and attendance updating |

---

## 3. Technology Stack

* **Backend:** Java 17 LTS, Spring Boot 3.2.5 (Spring MVC, Spring Data JPA / Hibernate ORM)
* **Build System:** Apache Maven (includes `mvnw` and `mvnw.cmd` wrappers)
* **Database:** MySQL 8.0+ (`student_db` schema with `ON DELETE CASCADE` referential integrity)
* **Frontend:** Thymeleaf template engine, HTML5, CSS3 (Custom design system in `style.css`), Bootstrap 5.3, Font Awesome 6
* **Visualizations:** Chart.js 4.4 (Department distribution doughnut chart and pass/fail analytics bar chart)
* **Security & Auth:** Spring Security Crypto (`BCryptPasswordEncoder`) + HTTP session interceptor (`AuthInterceptor`)

---

## 4. Quick Setup & Execution Guide

### Step 1: Prerequisites
Ensure you have the following installed:
1. **Java Development Kit (JDK 17 LTS or higher)**
   Verify in terminal: `java -version`
2. **MySQL Server 8.0 or MariaDB** (Running on `localhost:3306`)
   Verify in terminal: `mysql -u root -p`
3. **Maven** (Optional &ndash; you can use the bundled `./mvnw` or `mvnw.cmd` wrapper directly)

---

### Step 2: Database Initialization (MySQL)

1. Open **MySQL Workbench**, **phpMyAdmin**, or your terminal shell:
   ```bash
   mysql -u root -p
   ```
2. Execute the provided `schema.sql` script located in the project root:
   ```sql
   SOURCE schema.sql;
   ```
   *(Or copy-paste the contents of `schema.sql` directly into MySQL Workbench query tab and click Execute).*

3. Verify that database `student_db` has been created with 12 seeded students and default users:
   ```sql
   USE student_db;
   SELECT COUNT(*) FROM students; -- Returns 12
   SELECT * FROM users;          -- Returns admin and teacher
   ```

---

### Step 3: Configure Database Connection
Configure the database with environment variables instead of committing credentials:
```properties
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/student_db?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true&createDatabaseIfNotExist=true
SPRING_DATASOURCE_USERNAME=root
SPRING_DATASOURCE_PASSWORD=your-mysql-password
```
The `MYSQLHOST`, `MYSQLPORT`, `MYSQLDATABASE`, `MYSQLUSER`, and `MYSQLPASSWORD` variables are also supported for MySQL hosting services that provide them.

> **Zero-Setup Quick Evaluation Mode (Recommended):**
> If MySQL is not running on your machine, launch the application with the in-memory H2 database profile. It creates the tables and demo accounts automatically; MySQL is not required.
> ```bash
> ./mvnw spring-boot:run -Dspring-boot.run.profiles=h2
> ```
> On Windows PowerShell:
> ```powershell
> .\mvnw.cmd spring-boot:run "-Dspring-boot.run.profiles=h2"
> ```
> With this profile, open `http://localhost:8080` and sign in with `admin` / `admin123`.

---

### Step 4: Build and Run Application
In your project root directory (`OPPS MINI PROJECT STUD MANA`), execute:

**On Windows (PowerShell / Command Prompt):**
```cmd
mvn spring-boot:run
```
*Or using the Maven wrapper:*
```cmd
.\mvnw.cmd spring-boot:run
```

**On Linux / macOS:**
```bash
./mvnw spring-boot:run
```

---

### Step 5: Access the ERP Web Portal
Open any modern web browser (Chrome, Edge, Firefox, Safari) and navigate to:
```
http://localhost:8082
```
1. You will be greeted by the **Apex Institute of Technology ERP Login Portal**.
2. Log in with **Username:** `admin` and **Password:** `admin123`.
3. Explore the **Dashboard, Student Directory, Marks Entry, Attendance Tracking, and Official Marksheets**!

---

## 5. Deploy the Full Application

This is a Java Spring Boot application that renders its pages on the server and connects directly to a SQL database. Netlify cannot run the existing Java application as a static site. Deploy the included Docker image to a Java/container host instead; Railway with its MySQL service is one option. The same Docker image can run on Render or another Docker-compatible host with an externally hosted MySQL database.

### Railway with MySQL

1. Push the project to a GitHub repository and create a Railway project from that repository. Railway builds and runs the root [`Dockerfile`](Dockerfile).
2. Add a Railway MySQL service to the project.
3. On the application service, set `SPRING_PROFILES_ACTIVE` to `prod`.
4. Set the initial account credentials on the application service. Use unique passwords of at least 12 characters:

   | Variable | Example username/value |
   | :--- | :--- |
   | `APP_BOOTSTRAP_ADMIN_USERNAME` | `admin` |
   | `APP_BOOTSTRAP_ADMIN_PASSWORD` | Set a unique secret of at least 12 characters |
   | `APP_BOOTSTRAP_TEACHER_USERNAME` | `teacher` |
   | `APP_BOOTSTRAP_TEACHER_PASSWORD` | Set a different unique secret of at least 12 characters |

5. Link the MySQL service's `MYSQLHOST`, `MYSQLPORT`, `MYSQLDATABASE`, `MYSQLUSER`, and `MYSQLPASSWORD` variables to the application service. The production profile builds the JDBC connection from these variables. Alternatively, set `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, and `SPRING_DATASOURCE_PASSWORD` directly.
6. Generate a public domain for the application service and open it. Railway supplies `PORT` automatically; the application listens on it. `/login` is available as an HTTP health-check path.

The `prod` profile fails startup if bootstrap account credentials are missing or either password is shorter than 12 characters. Admin and teacher accounts are created only when their usernames do not already exist; changing bootstrap variables later does **not** change existing passwords. Use a persistent MySQL database: the H2 demo database is in-memory and is not suitable for deployment or persistent student records.

### Build the Docker image locally (optional)

```bash
docker build -t college-student-management .
docker run --rm -p 8080:8080 --env-file .env college-student-management
```

For a production-profile local run, put `SPRING_PROFILES_ACTIVE=prod`, MySQL connection variables, and all four bootstrap-account variables in your local `.env` file. Never commit `.env` or production secrets.

---

## 6. Core Features & System Walkthrough

### 1. Executive Dashboard (`/dashboard`)
* **Metric Cards:** Real-time counts of Total Students, Departments Count, Average Attendance %, and Passed vs Failed ratio.
* **Statutory Alert:** Dynamic indicator showing count of students below the mandatory 75% attendance threshold.
* **Interactive Chart.js Visualizations:**
  * *Department Distribution Doughnut Chart* (CSE, IT, AI&DS, ENTC, Mechanical, Civil).
  * *Pass vs Fail Bar Chart* reflecting university academic criteria.
* **Quick ERP Action Bar:** Immediate one-click navigation to common tasks.
* **Recent Registrations:** Overview table of newly admitted students.

### 2. Enroll New Student (`/students/add`)
* Multi-section admission form capturing academic details, personal details (Person base class), and contact records.
* **Dropdowns:** Departments (`CSE`, `IT`, `AI&DS`, `ENTC`, `Mechanical`, `Civil`) and Class Years (`FE`, `SE`, `TE`, `BE`).
* **Validation Rules:**
  * Mandatory field constraints.
  * Unique Student Roll ID (e.g., `STU2024001`) with duplicate prevention.
  * Strict 10-digit mobile phone pattern validation.
  * Unique, well-formed email validation.
* Automatically initializes 5 curriculum subject marks and attendance records upon creation.

### 3. Student Directory & Search (`/students` & `/students/search`)
* Tabular view with server-side pagination, record size indicators, and multi-column sorting (by Student ID, Name, Department).
* **Dedicated Search Page (`/students/search`):** Demonstrates **Polymorphism (Method Overloading)**.
  * Searches by numerical ID or partial name matching.
  * Optional Department filter.
  * Clean **"No record found"** empty-state card with one-click search reset if no students match the query.
* **Delete Modal:** Bootstrap 5 confirmation modal displaying the student's name and roll number before confirming database cascading deletion.

### 4. Curriculum Marks Entry (`/marks/entry/{id}`)
* Form allowing entry of scores for the 5 curriculum subjects:
  1. *Object Oriented Programming (OOP)*
  2. *Database Management Systems (DBMS)*
  3. *Data Structures & Algorithms (DSA)*
  4. *Computer Networks (CN)*
  5. *Operating Systems (OS)*
* **Validation:** $0.0 \le \text{marks} \le 100.0$ boundary check. Custom `InvalidMarksException` triggered if boundaries are violated.
* **Live Calculation:** JavaScript calculator dynamically tallies total score and percentage in real-time as marks are typed.

### 5. Attendance Management & Shortage Alert (`/attendance` & `/attendance/entry/{id}`)
* Records `total_classes` and `attended_classes`.
* **Automated Calculation:** Live formula $\frac{\text{attended}}{\text{total}} \times 100$.
* **Compliance Threshold:**
  * $\ge 75\%$: Displayed with green badge `Satisfactory (Eligible for Exams)`.
  * $< 75\%$: Flagged with an animated pulsing **red badge `Shortage (<75%)`** with official warning message.

### 6. Official Academic Marksheet & Transcript (`/reports/view/{id}`)
* Official institutional grade statement formatted with university crest (`logo.svg`), NAAC A+ accreditation credentials, and student particulars.
* **Passing Rule:** A student is marked **PASS** if and only if **aggregate percentage $\ge 40\%$ AND every individual subject score $\ge 35$**.
* **Grading System:**
  * $O$ ($\ge 90\%$) &ndash; Outstanding
  * $A+$ ($\ge 80\%$) &ndash; Excellent
  * $A$ ($\ge 70\%$) &ndash; Very Good
  * $B$ ($\ge 60\%$) &ndash; Good
  * $C$ ($\ge 50\%$) &ndash; Average
  * $D$ ($\ge 40\%$) &ndash; Pass
  * $F$ ($< 40\%$ or any subject $< 35$) &ndash; Fail
* **Print / Download PDF:** One-click print button configured with dedicated `@media print` CSS that strips navigation bars, sidebars, and buttons, generating a clean paper transcript with official signature lines for *Prepared By*, *Head of Department*, and *Controller of Examinations*.

---

## 6. Project Directory Structure

```
OPPS MINI PROJECT STUD MANA/
├── pom.xml                                  # Maven dependencies & build configuration
├── schema.sql                               # MySQL DDL schema + 12 sample students seed script
├── CLASS_DIAGRAM.puml                       # PlantUML Class Diagram source
├── ER_DIAGRAM.md                            # Entity-Relationship diagram & table specifications
├── README.md                                # Comprehensive project guide & viva notes
├── mvnw                                     # Linux/macOS Maven wrapper script
├── mvnw.cmd                                 # Windows batch Maven wrapper script
├── .mvn/wrapper/
│   └── maven-wrapper.properties             # Apache Maven 3.9.6 wrapper distribution config
└── src/
    └── main/
        ├── java/com/college/sms/
        │   ├── StudentManagementSystemApplication.java   # Spring Boot Main Application Class
        │   ├── config/
        │   │   └── DataInitializer.java     # Seeds admin user & 12 sample students on startup
        │   ├── controller/
        │   │   ├── AuthController.java      # Login, session auth, logout
        │   │   ├── DashboardController.java # Dashboard metrics & Chart.js endpoints
        │   │   ├── StudentController.java   # Student CRUD, pagination, sorting, search
        │   │   ├── MarkController.java      # 5-subject marks entry & validation
        │   │   ├── AttendanceController.java# Attendance tracking & shortage alerts
        │   │   ├── ReportController.java    # Academic transcripts & printable marksheets
        │   │   └── CustomErrorController.java# 404, 500 error mapping
        │   ├── exception/
        │   │   ├── StudentNotFoundException.java   # Custom unchecked domain exception
        │   │   ├── InvalidMarksException.java      # Custom unchecked domain exception
        │   │   ├── DuplicateStudentException.java  # Custom unchecked domain exception
        │   │   └── GlobalExceptionHandler.java     # @ControllerAdvice centralized handler
        │   ├── interceptor/
        │   │   ├── AuthInterceptor.java     # Session-based route protection
        │   │   └── WebMvcConfig.java        # Spring MVC interceptor & asset registry
        │   ├── model/
        │   │   ├── Person.java              # Inheritance base class (Encapsulation)
        │   │   ├── Student.java             # Extends Person, implements Reportable (Polymorphism)
        │   │   ├── Reportable.java          # Abstraction interface
        │   │   ├── StudentOperations.java   # Abstraction interface
        │   │   ├── User.java                # Authentication user entity
        │   │   ├── Role.java                # ADMIN, TEACHER role enumeration
        │   │   ├── Mark.java                # Subject mark entity with bounded setter
        │   │   ├── Attendance.java          # Attendance record entity
        │   │   └── AcademicReport.java      # View DTO for transcript generation
        │   ├── repository/
        │   │   ├── UserRepository.java      # Spring Data JPA repository
        │   │   ├── StudentRepository.java   # Custom search, pagination, and grouping queries
        │   │   ├── MarkRepository.java      # Subject marks persistence
        │   │   └── AttendanceRepository.java# Attendance persistence & average calculations
        │   ├── service/
        │   │   ├── StudentService.java      # Abstraction with Method Overloading
        │   │   ├── UserService.java         # Authentication service abstraction
        │   │   ├── MarkService.java         # Marks service abstraction
        │   │   ├── AttendanceService.java   # Attendance service abstraction
        │   │   ├── ReportService.java       # Transcript computation service abstraction
        │   │   ├── DashboardService.java    # Dashboard metrics service abstraction
        │   │   └── impl/
        │   │       ├── StudentServiceImpl.java
        │   │       ├── UserServiceImpl.java
        │   │       ├── MarkServiceImpl.java
        │   │       ├── AttendanceServiceImpl.java
        │   │       ├── ReportServiceImpl.java
        │   │       └── DashboardServiceImpl.java
        │   └── util/
        │       ├── AppConstants.java        # Static final global constants
        │       ├── GradeCalculator.java     # Static utility methods for grading
        │       └── PasswordUtil.java        # BCrypt salted hashing utility
        └── resources/
            ├── application.properties       # Primary configuration (MySQL localhost:3306)
            ├── application-h2.properties    # Optional fallback profile for in-memory testing
            ├── schema.sql                   # Embedded copy of database schema
            ├── static/
            │   ├── css/
            │   │   └── style.css            # Responsive ERP design system & @media print styles
            │   ├── js/
            │   │   └── main.js              # Live attendance %, marks sum, delete modal binding
            │   └── images/
            │       ├── logo.svg             # Official vector university crest
            │       ├── campus.svg           # University architectural hero illustration
            │       ├── classroom.svg        # Academic lecture hall illustration
            │       ├── graduation.svg       # Convocation ceremony illustration
            │       └── avatar.svg           # Administrator avatar icon
            └── templates/
                ├── layout/
                │   └── main.html            # Master layout (Navbar, Sidebar, Footer, Modals)
                ├── auth/
                │   └── login.html           # Campus background login page with credentials box
                ├── dashboard.html           # Metric cards, Chart.js charts, recent students
                ├── students/
                │   ├── list.html            # Paginated table, sortable columns, action buttons
                │   ├── add.html             # Enrollment form with validations & dropdowns
                │   ├── edit.html            # Pre-filled student update form
                │   └── search.html          # Overloaded search with "No record found" alert
                ├── marks/
                │   ├── list.html            # Subject averages summary & roster
                │   └── entry.html           # 5-subject marks entry with live total
                ├── attendance/
                │   ├── list.html            # Attendance register with <75% red flags
                │   └── entry.html           # Live attendance % calculation & alert
                ├── reports/
                │   ├── index.html           # Student grade report directory
                │   └── report.html          # Official transcript marksheet with Print/PDF
                └── error/
                    ├── 404.html             # Styled 404 record not found view
                    ├── 500.html             # Styled 500 internal server error view
                    └── error.html           # Generic error template
```

---

## 7. Screenshots Presentation List (For Project Viva / Submission)

When submitting project reports or demonstrating in front of an external examiner, capture the following 10 views:

1. **ERP Login Page:** Campus architectural background, clean login card with pre-filled default credentials reminder (`admin`/`admin123`).
2. **Executive Dashboard:** Campus hero banner, 4 stat cards (Total Students, Departments, Avg Attendance %, Pass/Fail), Department Distribution Doughnut Chart, Pass vs Fail Bar Chart, and Recent Students table.
3. **Enroll Student Form:** Validation in action showing required field asterisks, department select dropdown, class year select, and 10-digit phone enforcement.
4. **Student Directory Table:** Paginated table showing 12 diverse student records across FE, SE, TE, and BE with department tags and attendance status badges.
5. **Search Student Page & "No record found" State:** Demonstrating query by name/ID, department filter, and the prominent warning message when no record matches.
6. **Curriculum Marks Management Roster:** System-wide subject average cards (OOP, DBMS, DSA, CN, OS) and student marks status badges.
7. **5-Subject Marks Entry Form:** Input fields with range boundaries (0-100), passing score guidelines, and live total score tallying.
8. **Attendance Register & Shortage Flagging:** Student list highlighting students with attendance $\ge 75\%$ in green and $< 75\%$ in animated **red badges**.
9. **Attendance Entry with Live Calculator:** Showing dynamic calculation as numbers are entered into total and attended class fields.
10. **Official Academic Marksheet / Print Preview:** Full transcript with university crest, candidate information table, subject marks breakdown, aggregate percentage, letter grade ($O$, $A+$, $A$, $B$, $C$, $D$, $F$), Pass/Fail verdict, and official signature blocks.
