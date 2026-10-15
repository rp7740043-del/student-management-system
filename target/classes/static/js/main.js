/**
 * College Student Management System - Client Side Interactivity
 */

document.addEventListener('DOMContentLoaded', function () {

    // 1. Sidebar Toggle for Mobile Devices
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.getElementById('appSidebar');

    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
    }

    // 2. Auto-Dismiss Flash Alert Messages
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // 3. Delete Modal Confirmation Dynamic Binding
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const studentId = button.getAttribute('data-student-id');
            const studentName = button.getAttribute('data-student-name');
            const deleteForm = document.getElementById('deleteStudentForm');
            const studentNameSpan = document.getElementById('deleteStudentNameSpan');

            if (deleteForm && studentId) {
                deleteForm.action = '/students/delete/' + studentId;
            }
            if (studentNameSpan && studentName) {
                studentNameSpan.textContent = studentName;
            }
        });
    }

    // 4. Live Attendance % Calculation on Attendance Entry Form
    const totalClassesInput = document.getElementById('totalClasses');
    const attendedClassesInput = document.getElementById('attendedClasses');
    const attendancePctPreview = document.getElementById('attendancePctPreview');
    const attendanceAlertBox = document.getElementById('attendanceAlertBox');

    function updateAttendancePreview() {
        if (!totalClassesInput || !attendedClassesInput || !attendancePctPreview) return;

        const total = parseFloat(totalClassesInput.value) || 0;
        const attended = parseFloat(attendedClassesInput.value) || 0;

        if (total <= 0) {
            attendancePctPreview.textContent = '0.00%';
            attendancePctPreview.className = 'badge bg-secondary';
            if (attendanceAlertBox) attendanceAlertBox.style.display = 'none';
            return;
        }

        if (attended > total) {
            attendancePctPreview.textContent = 'Invalid: Attended > Total';
            attendancePctPreview.className = 'badge bg-danger';
            if (attendanceAlertBox) {
                attendanceAlertBox.style.display = 'block';
                attendanceAlertBox.className = 'alert alert-danger';
                attendanceAlertBox.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Attended classes cannot be greater than total classes!';
            }
            return;
        }

        const pct = (attended / total) * 100;
        const rounded = pct.toFixed(2);
        attendancePctPreview.textContent = rounded + '%';

        if (pct < 75.0) {
            attendancePctPreview.className = 'badge bg-danger';
            if (attendanceAlertBox) {
                attendanceAlertBox.style.display = 'block';
                attendanceAlertBox.className = 'alert alert-danger';
                attendanceAlertBox.innerHTML = '<i class="fas fa-exclamation-circle me-2"></i><strong>Warning: Shortage of Attendance!</strong> Attendance is below mandatory 75% threshold.';
            }
        } else {
            attendancePctPreview.className = 'badge bg-success';
            if (attendanceAlertBox) {
                attendanceAlertBox.style.display = 'block';
                attendanceAlertBox.className = 'alert alert-success';
                attendanceAlertBox.innerHTML = '<i class="fas fa-check-circle me-2"></i>Attendance is satisfactory (>= 75%). Eligible for University Examinations.';
            }
        }
    }

    if (totalClassesInput && attendedClassesInput) {
        totalClassesInput.addEventListener('input', updateAttendancePreview);
        attendedClassesInput.addEventListener('input', updateAttendancePreview);
        // Initial run
        updateAttendancePreview();
    }

    // 5. Live Marks Total & Average Calculator
    const markInputs = document.querySelectorAll('.subject-mark-input');
    const totalScoreDisplay = document.getElementById('liveTotalScore');
    const avgScoreDisplay = document.getElementById('liveAvgScore');

    function updateMarksPreview() {
        if (markInputs.length === 0 || !totalScoreDisplay) return;

        let total = 0;
        let count = 0;
        let anyFail = false;

        markInputs.forEach(function (input) {
            const val = parseFloat(input.value);
            if (!isNaN(val)) {
                total += val;
                count++;
                if (val < 35) anyFail = true;
            }
        });

        totalScoreDisplay.textContent = total.toFixed(1);
        if (avgScoreDisplay) {
            const avg = count > 0 ? (total / (count * 100)) * 100 : 0;
            avgScoreDisplay.textContent = avg.toFixed(2) + '%';
        }
    }

    markInputs.forEach(function (input) {
        input.addEventListener('input', updateMarksPreview);
    });
});
