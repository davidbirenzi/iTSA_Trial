from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    
    # Authentication URLs
    path('student/login/', views.login_student, name='login_student'),
    path('student/register/', views.register_student, name='register_student'),
    path('teacher/login/', views.login_teacher, name='login_teacher'),
    path('teacher/register/', views.register_teacher, name='register_teacher'),
    path('logout/', views.logout_view, name='logout'),
    
    # Student URLs
    path('student/home/', views.student_home, name='student_home'),
    path('student/level-one/', views.level_one, name='level_one'),
    path('student/level-one/start/', views.start_level_one, name='start_level_one'),
    path('student/level-one/quiz/', views.quiz_level_one, name='quiz_level_one'),
    path('student/level-one/submit/', views.submit_quiz_one, name='submit_quiz_one'),
    
    # Teacher URLs
    path('teacher/home/', views.teacher_home, name='teacher_home'),
    path('teacher/students/', views.teacher_students, name='teacher_students'),
    path('teacher/courses/', views.teacher_courses, name='teacher_courses'),
    path('teacher/course/upload/', views.upload_course, name='upload_course'),
    path('teacher/course/<int:course_id>/outcome/upload/', views.upload_learning_outcome, name='upload_learning_outcome'),
] 