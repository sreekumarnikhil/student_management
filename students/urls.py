from django.urls import path
from . import views

urlpatterns = [ 

    path('students/', views.student_list , name = 'student_list'),
    path('students/add/' , views.add_student , name = 'add_student'),
    path('students/edit/<int:id>/', views.edit_student , name = 'edit_student'),
    path('students/delete/<int:id>/', views.delete_student , name = 'delete_student'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:id>/', views.delete_course, name='delete_course'),
    path('', views.dashboard, name='dashboard'),
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/add/', views.add_enrollment, name='add_enrollment'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('marks/', views.mark_list, name='mark_list'),
    path('marks/add/', views.add_mark, name='add_mark'),  
]