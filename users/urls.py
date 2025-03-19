from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('student/register/', views.register_student, name='register_student'),
    path('student/login/', views.login_student, name='login_student'),
    path('student/home/', views.student_home, name='student_home'),
    
    # Teacher URLs
    path('teacher/register/', views.register_teacher, name='register_teacher'),
    path('teacher/login/', views.login_teacher, name='login_teacher'),
    path('teacher/home/', views.teacher_home, name='teacher_home'),
    path('teacher/students/', views.teacher_students, name='teacher_students'),
    path('teacher/courses/', views.teacher_courses, name='teacher_courses'),
    path('teacher/upload-course/', views.upload_course, name='upload_course'),
    path('teacher/upload-learning-outcome/<int:course_id>/', views.upload_learning_outcome, name='upload_learning_outcome'),
    
    # Logout URL
    path('logout/', views.logout_view, name='logout'),
] 