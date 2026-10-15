from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20 , unique = True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.course_name        

class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE
    )
    enrollment_date = models.DateField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course'
            )
        ]

    def _str_(self):
        return f"{self.student.name} - {self.course.course_name}"


class Attendance(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE
    )
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent'),
            ('Late', 'Late'),
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['enrollment', 'date'],
                name='unique_enrollment_attendance_date'
            )
        ]

    def _str_(self):
        return f"{self.enrollment} - {self.date}"


class Mark(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE
    )
    assessment_name = models.CharField(max_length=100)
    marks_obtained = models.DecimalField(
        max_digits=7, decimal_places=2
    )
    total_marks = models.DecimalField(
        max_digits=7, decimal_places=2
    )

    def _str_(self):
        return f"{self.enrollment} - {self.assessment_name}"        