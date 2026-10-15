from django.shortcuts import render , redirect
from .models import Student , Course ,  Enrollment , Attendance , Mark
from django.db import models
from django.shortcuts import get_object_or_404


def student_list(request):
    search_query = request.GET.get('q', '').strip()

    students = Student.objects.all()

    if search_query:
        students = students.filter(
            models.Q(name__icontains=search_query) |
            models.Q(student_id__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(course__icontains=search_query)
        )

    return render(
        request,
        'student_list.html',
        {
            'students': students,
            'search_query': search_query
        }
    )

def add_student(request):
    error = ''

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        course = request.POST.get('course', '').strip()

        if not all([student_id, name, email, phone, course]):
            error = 'All fields are required.'

        elif Student.objects.filter(student_id=student_id).exists():
            error = 'Student ID already exists.'

        else:
            Student.objects.create(
                student_id=student_id,
                name=name,
                email=email,
                phone=phone,
                course=course
            )
            return redirect('student_list')

    return render(request, 'add_student.html', {'error': error})


def edit_student(request, id):
    student = Student.objects.get(id=id)
    error = ''

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        course = request.POST.get('course', '').strip()

        if not all([student_id, name, email, phone, course]):
            error = 'All fields are required.'

        elif Student.objects.filter(
            student_id=student_id
        ).exclude(id=id).exists():
            error = 'Student ID already exists.'

        else:
            student.student_id = student_id
            student.name = name
            student.email = email
            student.phone = phone
            student.course = course
            student.save()

            return redirect('student_list')

    return render(
        request,
        'edit_student.html',
        {'student': student, 'error': error}
    )

def delete_student(request, id):
      if request.method == 'POST':
        student = get_object_or_404(Student, id=id)
        student.delete()

      return redirect('student_list')   

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {
        'courses': courses
    })


def add_course(request):
    error = ''

    if request.method == 'POST':
        course_id = request.POST.get('course_id', '').strip()
        course_name = request.POST.get('course_name', '').strip()
        duration = request.POST.get('duration', '').strip()
        description = request.POST.get('description', '').strip()

        if not course_id or not course_name or not duration:
            error = 'Please fill in all required fields.'

        elif Course.objects.filter(course_id=course_id).exists():
            error = 'Course ID already exists.'

        else:
            Course.objects.create(
                course_id=course_id,
                course_name=course_name,
                duration=duration,
                description=description
            )
            return redirect('course_list')

    return render(request, 'add_course.html', {'error': error})      

def edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    error = ''

    if request.method == 'POST':
        course_id = request.POST.get('course_id', '').strip()
        course_name = request.POST.get('course_name', '').strip()
        duration = request.POST.get('duration', '').strip()
        description = request.POST.get('description', '').strip()

        if not course_id or not course_name or not duration:
            error = 'Please fill in all required fields.'

        elif Course.objects.filter(
            course_id=course_id
        ).exclude(id=id).exists():
            error = 'Course ID already exists.'

        else:
            course.course_id = course_id
            course.course_name = course_name
            course.duration = duration
            course.description = description
            course.save()

            return redirect('course_list')

    return render(request, 'edit_course.html', {
        'course': course,
        'error': error
    })


def delete_course(request, id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=id)
        course.delete()

    return redirect('course_list')    

def dashboard(request):
    return render(request, 'dashboard.html', {
        'student_count': Student.objects.count(),
        'course_count': Course.objects.count(),
        'enrollment_count': Enrollment.objects.count(),
        'attendance_count': Attendance.objects.count(),
        'mark_count': Mark.objects.count(),
    })


def enrollment_list(request):
    enrollments = Enrollment.objects.select_related(
        'student', 'course'
    ).all()

    return render(request, 'enrollment_list.html', {
        'enrollments': enrollments
    })


def add_enrollment(request):
    error = ''

    if request.method == 'POST':
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')

        if not student_id or not course_id:
            error = 'Please select a student and course.'
        else:
            student = get_object_or_404(Student, id=student_id)
            course = get_object_or_404(Course, id=course_id)

            if Enrollment.objects.filter(
                student=student, course=course
            ).exists():
                error = 'This student is already enrolled in this course.'
            else:
                Enrollment.objects.create(
                    student=student, course=course
                )
                return redirect('enrollment_list')

    return render(request, 'add_enrollment.html', {
        'students': Student.objects.all(),
        'courses': Course.objects.all(),
        'error': error,
    })


def attendance_list(request):
    attendance_records = Attendance.objects.all().order_by('-date')

    return render(request, 'attendance_list.html', {
        'attendance_records': attendance_records
    })


def add_attendance(request):
    error = ''

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment')
        date = request.POST.get('date')
        status = request.POST.get('status')

        if not enrollment_id or not date or status not in [
            'Present', 'Absent', 'Late'
        ]:
            error = 'Please complete all fields.'
        else:
            enrollment = get_object_or_404(
                Enrollment, id=enrollment_id
            )

            if Attendance.objects.filter(
                enrollment=enrollment, date=date
            ).exists():
                error = 'Attendance already exists for this date.'
            else:
                Attendance.objects.create(
                    enrollment=enrollment,
                    date=date,
                    status=status
                )
                return redirect('attendance_list')

    return render(request, 'add_attendance.html', {
        'enrollments': Enrollment.objects.select_related(
            'student', 'course'
        ).all(),
        'error': error,
    })


def mark_list(request):
    marks = Mark.objects.all()

    return render(request, 'mark_list.html', {
        'marks': marks
    })


def add_mark(request):
    error = ''

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment')
        assessment_name = request.POST.get(
            'assessment_name', ''
        ).strip()
        obtained = request.POST.get('marks_obtained', '')
        total = request.POST.get('total_marks', '')

        if not all([enrollment_id, assessment_name, obtained, total]):
            error = 'Please complete all fields.'
        else:
            try:
                obtained_value = float(obtained)
                total_value = float(total)

                if total_value <= 0 or obtained_value < 0:
                    error = 'Marks must be valid positive values.'
                elif obtained_value > total_value:
                    error = 'Obtained marks cannot exceed total marks.'
                else:
                    enrollment = get_object_or_404(
                        Enrollment, id=enrollment_id
                    )
                    Mark.objects.create(
                        enrollment=enrollment,
                        assessment_name=assessment_name,
                        marks_obtained=obtained_value,
                        total_marks=total_value
                    )
                    return redirect('mark_list')

            except ValueError:
                error = 'Please enter valid numeric marks.'

    return render(request, 'add_mark.html', {
        'enrollments': Enrollment.objects.select_related(
            'student', 'course'
        ).all(),
        'error': error,
    })    