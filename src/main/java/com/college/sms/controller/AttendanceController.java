package com.college.sms.controller;

import com.college.sms.exception.StudentNotFoundException;
import com.college.sms.model.Attendance;
import com.college.sms.model.Student;
import com.college.sms.service.AttendanceService;
import com.college.sms.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;

/**
 * Controller managing student attendance metrics and shortages (< 75%).
 */
@Controller
@RequestMapping("/attendance")
public class AttendanceController {

    private final AttendanceService attendanceService;
    private final StudentService studentService;

    @Autowired
    public AttendanceController(AttendanceService attendanceService, StudentService studentService) {
        this.attendanceService = attendanceService;
        this.studentService = studentService;
    }

    // =========================================================================
    // Attendance Overview List
    // =========================================================================
    @GetMapping
    public String listAttendance(Model model) {
        List<Student> students = studentService.getAllStudents();
        double overallAverage = attendanceService.getOverallAverageAttendance();

        model.addAttribute("students", students);
        model.addAttribute("overallAverage", overallAverage);
        model.addAttribute("activePage", "attendance");
        return "attendance/list";
    }

    // =========================================================================
    // Attendance Entry Form
    // =========================================================================
    @GetMapping("/entry/{id}")
    public String showAttendanceEntryForm(@PathVariable("id") Long id, Model model) {
        Student student = studentService.findById(id)
                .orElseThrow(() -> new StudentNotFoundException(id));

        Attendance attendance = attendanceService.getAttendanceForStudent(student.getId())
                .orElse(new Attendance(student, 0, 0));

        model.addAttribute("student", student);
        model.addAttribute("attendance", attendance);
        model.addAttribute("activePage", "attendance");
        return "attendance/entry";
    }

    @PostMapping("/entry/{id}")
    public String saveAttendance(@PathVariable("id") Long id,
                                 @RequestParam("totalClasses") int totalClasses,
                                 @RequestParam("attendedClasses") int attendedClasses,
                                 RedirectAttributes redirectAttributes) {
        Student student = studentService.findById(id)
                .orElseThrow(() -> new StudentNotFoundException(id));

        try {
            attendanceService.saveOrUpdateAttendance(student.getId(), totalClasses, attendedClasses);
            redirectAttributes.addFlashAttribute("successMessage", 
                    "Attendance for student '" + student.getName() + "' updated successfully!");
            return "redirect:/attendance";

        } catch (IllegalArgumentException ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
            return "redirect:/attendance/entry/" + id;
        }
    }
}
