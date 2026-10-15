package com.college.sms.config;

import com.college.sms.model.*;
import com.college.sms.repository.AttendanceRepository;
import com.college.sms.repository.MarkRepository;
import com.college.sms.repository.StudentRepository;
import com.college.sms.repository.UserRepository;
import com.college.sms.service.UserService;
import com.college.sms.util.AppConstants;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;

/**
 * Automatically seeds initial administrative accounts and sample student records
 * if the database is initially empty. Ensures the project runs out-of-the-box.
 */
@Component
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final UserService userService;
    private final StudentRepository studentRepository;
    private final MarkRepository markRepository;
    private final AttendanceRepository attendanceRepository;
    private final String adminUsername;
    private final String adminPassword;
    private final String teacherUsername;
    private final String teacherPassword;
    private final boolean requireStrongBootstrapPasswords;

    @Autowired
    public DataInitializer(UserRepository userRepository, 
                           UserService userService, 
                           StudentRepository studentRepository, 
                           MarkRepository markRepository, 
                           AttendanceRepository attendanceRepository,
                           @Value("${app.bootstrap.admin.username:admin}") String adminUsername,
                           @Value("${app.bootstrap.admin.password:admin123}") String adminPassword,
                           @Value("${app.bootstrap.teacher.username:teacher}") String teacherUsername,
                           @Value("${app.bootstrap.teacher.password:teacher123}") String teacherPassword,
                           @Value("${app.bootstrap.require-strong-passwords:false}") boolean requireStrongBootstrapPasswords) {
        this.userRepository = userRepository;
        this.userService = userService;
        this.studentRepository = studentRepository;
        this.markRepository = markRepository;
        this.attendanceRepository = attendanceRepository;
        this.adminUsername = adminUsername;
        this.adminPassword = adminPassword;
        this.teacherUsername = teacherUsername;
        this.teacherPassword = teacherPassword;
        this.requireStrongBootstrapPasswords = requireStrongBootstrapPasswords;
    }

    @Override
    public void run(String... args) {
        seedUsers();
        seedStudents();
    }

    private void seedUsers() {
        requireBootstrapCredential("admin", adminUsername, adminPassword);
        requireBootstrapCredential("teacher", teacherUsername, teacherPassword);

        if (!userRepository.existsByUsername(adminUsername)) {
            User admin = new User(adminUsername, adminPassword, Role.ADMIN);
            userService.registerUser(admin);
            System.out.println(">>> Initialized Admin user: " + adminUsername);
        }

        if (!userRepository.existsByUsername(teacherUsername)) {
            User teacher = new User(teacherUsername, teacherPassword, Role.TEACHER);
            userService.registerUser(teacher);
            System.out.println(">>> Initialized Teacher user: " + teacherUsername);
        }
    }

    private void requireBootstrapCredential(String role, String username, String password) {
        if (username == null || username.isBlank()) {
            throw new IllegalStateException("Set a nonblank bootstrap username for the " + role + " account.");
        }
        if (password == null || password.isBlank()
                || (requireStrongBootstrapPasswords && password.length() < 12)) {
            throw new IllegalStateException("Set a bootstrap password of at least 12 characters for the " + role + " account.");
        }
    }

    private void seedStudents() {
        if (studentRepository.count() == 0) {
            System.out.println(">>> Seeding 12 sample students with realistic marks and attendance...");

            // Define student dataset
            List<StudentSeedData> seedData = Arrays.asList(
                new StudentSeedData("STU2024001", "Aarav Sharma", "CSE", "TE", "aarav.sharma@college.edu", "9876543210",
                        "124 MG Road, Pune, Maharashtra", LocalDate.of(2003, 5, 14), "Male", LocalDate.of(2022, 8, 1),
                        new double[]{88.0, 92.0, 85.0, 78.0, 84.0}, 120, 108),

                new StudentSeedData("STU2024002", "Priya Patel", "IT", "TE", "priya.patel@college.edu", "9823456781",
                        "45 Park Avenue, Mumbai, Maharashtra", LocalDate.of(2003, 8, 22), "Female", LocalDate.of(2022, 8, 1),
                        new double[]{95.0, 94.0, 91.0, 89.0, 93.0}, 120, 114),

                new StudentSeedData("STU2024003", "Rohan Verma", "AI&DS", "SE", "rohan.verma@college.edu", "9812345678",
                        "78 Shivaji Nagar, Pune, Maharashtra", LocalDate.of(2004, 2, 10), "Male", LocalDate.of(2023, 8, 10),
                        new double[]{72.0, 68.0, 75.0, 64.0, 70.0}, 120, 85),

                new StudentSeedData("STU2024004", "Ananya Deshmukh", "ENTC", "BE", "ananya.d@college.edu", "9890123456",
                        "12 Kothrud, Pune, Maharashtra", LocalDate.of(2002, 11, 5), "Female", LocalDate.of(2021, 8, 15),
                        new double[]{81.0, 85.0, 79.0, 88.0, 82.0}, 120, 102),

                new StudentSeedData("STU2024005", "Vikramaditya Singh", "Mechanical", "TE", "vikram.singh@college.edu", "9765432109",
                        "56 Model Colony, Pune, Maharashtra", LocalDate.of(2003, 7, 19), "Male", LocalDate.of(2022, 8, 1),
                        new double[]{62.0, 58.0, 65.0, 55.0, 60.0}, 120, 92),

                new StudentSeedData("STU2024006", "Sneha Kulkarni", "CSE", "FE", "sneha.k@college.edu", "9845123478",
                        "89 Baner Road, Pune, Maharashtra", LocalDate.of(2005, 3, 30), "Female", LocalDate.of(2024, 8, 5),
                        new double[]{78.0, 80.0, 82.0, 74.0, 76.0}, 100, 88),

                new StudentSeedData("STU2024007", "Aditi Rao", "Civil", "SE", "aditi.rao@college.edu", "9734567890",
                        "23 Koregaon Park, Pune, Maharashtra", LocalDate.of(2004, 9, 12), "Female", LocalDate.of(2023, 8, 10),
                        new double[]{55.0, 62.0, 58.0, 50.0, 54.0}, 120, 80),

                new StudentSeedData("STU2024008", "Rahul Joshi", "IT", "BE", "rahul.joshi@college.edu", "9822334455",
                        "67 Viman Nagar, Pune, Maharashtra", LocalDate.of(2002, 4, 18), "Male", LocalDate.of(2021, 8, 15),
                        new double[]{45.0, 48.0, 32.0, 40.0, 42.0}, 120, 72), // Failed in DSA (32 < 35)

                new StudentSeedData("STU2024009", "Tanvi Shinde", "AI&DS", "FE", "tanvi.s@college.edu", "9811223344",
                        "34 Aundh, Pune, Maharashtra", LocalDate.of(2005, 1, 25), "Female", LocalDate.of(2024, 8, 5),
                        new double[]{89.0, 91.0, 87.0, 85.0, 90.0}, 100, 94),

                new StudentSeedData("STU2024010", "Siddharth Mehta", "ENTC", "TE", "siddharth.m@college.edu", "9877889900",
                        "101 FC Road, Pune, Maharashtra", LocalDate.of(2003, 12, 8), "Male", LocalDate.of(2022, 8, 1),
                        new double[]{74.0, 70.0, 72.0, 68.0, 75.0}, 120, 100),

                new StudentSeedData("STU2024011", "Neha Gupta", "Mechanical", "BE", "neha.gupta@college.edu", "9866554433",
                        "15 Deccan Gymkhana, Pune, Maharashtra", LocalDate.of(2002, 6, 15), "Female", LocalDate.of(2021, 8, 15),
                        new double[]{65.0, 70.0, 68.0, 62.0, 66.0}, 120, 110),

                new StudentSeedData("STU2024012", "Harsh Vardhan", "Civil", "FE", "harsh.v@college.edu", "9855443322",
                        "88 Hadapsar, Pune, Maharashtra", LocalDate.of(2005, 8, 2), "Male", LocalDate.of(2024, 8, 5),
                        new double[]{38.0, 42.0, 40.0, 36.0, 41.0}, 100, 70)
            );

            for (StudentSeedData d : seedData) {
                Student s = new Student(null, d.name, d.email, d.phone, d.address, d.dob, d.gender,
                        d.studentId, d.department, d.classYear, d.admissionDate);
                Student savedStudent = studentRepository.save(s);

                // Add 5 subject marks
                for (int i = 0; i < AppConstants.DEFAULT_SUBJECTS.size(); i++) {
                    String sub = AppConstants.DEFAULT_SUBJECTS.get(i);
                    double score = (i < d.scores.length) ? d.scores[i] : 50.0;
                    Mark mark = new Mark(savedStudent, sub, score);
                    markRepository.save(mark);
                }

                // Add Attendance
                Attendance att = new Attendance(savedStudent, d.totalClasses, d.attendedClasses);
                attendanceRepository.save(att);
            }
            System.out.println(">>> Sample students, marks, and attendance seeded successfully.");
        }
    }

    private static class StudentSeedData {
        String studentId;
        String name;
        String department;
        String classYear;
        String email;
        String phone;
        String address;
        LocalDate dob;
        String gender;
        LocalDate admissionDate;
        double[] scores;
        int totalClasses;
        int attendedClasses;

        StudentSeedData(String studentId, String name, String department, String classYear, String email,
                        String phone, String address, LocalDate dob, String gender, LocalDate admissionDate,
                        double[] scores, int totalClasses, int attendedClasses) {
            this.studentId = studentId;
            this.name = name;
            this.department = department;
            this.classYear = classYear;
            this.email = email;
            this.phone = phone;
            this.address = address;
            this.dob = dob;
            this.gender = gender;
            this.admissionDate = admissionDate;
            this.scores = scores;
            this.totalClasses = totalClasses;
            this.attendedClasses = attendedClasses;
        }
    }
}
