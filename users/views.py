from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentLoginForm, TeacherRegistrationForm, TeacherLoginForm, CourseForm, LearningOutcomeForm
from .models import Course, TeacherUser, StudentUser

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login_teacher')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('student_home')
    else:
        form = StudentRegistrationForm()
    return render(request, 'users/register_student.html', {'form': form})

def login_student(request):
    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            student_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(student_email=student_email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('student_home')
    else:
        form = StudentLoginForm()
    return render(request, 'users/login_student.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('teacher_home')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'users/register_teacher.html', {'form': form})

def login_teacher(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, teacher_email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('teacher_home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = TeacherLoginForm()
    return render(request, 'users/login_teacher.html', {'form': form})

@login_required
def student_home(request):
    if not hasattr(request.user, 'student_email'):
        messages.error(request, 'Access denied. Student account required.')
        return redirect('login_student')
    return render(request, 'users/student_home.html')

@login_required
def teacher_home(request):
    if not hasattr(request.user, 'teacher_email'):
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('login_teacher')
    
    # Get all students in the teacher's faculty
    students = StudentUser.objects.filter(faculty=request.user.faculty)
    
    # Group students by cohort (academic year and trimester)
    cohorts = {}
    for student in students:
        cohort_key = f"Cohort {student.academic_year}-{student.trimester}"
        if cohort_key not in cohorts:
            cohorts[cohort_key] = []
        cohorts[cohort_key].append(student)
    
    # Calculate average scores for each cohort
    cohort_stats = {}
    for cohort_name, cohort_students in cohorts.items():
        total_score = sum(student.average_score for student in cohort_students if hasattr(student, 'average_score'))
        avg_score = total_score / len(cohort_students) if cohort_students else 0
        cohort_stats[cohort_name] = {
            'id': len(cohort_stats) + 1,
            'name': cohort_name,
            'average_score': round(avg_score, 2),
            'students': cohort_students
        }
    
    context = {
        'cohort_stats': cohort_stats,
    }
    return render(request, 'users/teacher_home.html', context)

@login_required
def teacher_students(request):
    if not hasattr(request.user, 'teacher_email'):
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('login_teacher')
    
    # Get the selected cohort from the URL
    selected_cohort = request.GET.get('cohort')
    if not selected_cohort:
        messages.error(request, 'No cohort selected.')
        return redirect('teacher_home')
    
    # Sample students with different scores
    sample_students = [
        {
            'student_email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'attempts': 3,
            'average_score': 85  # High score
        },
        {
            'student_email': 'jane.smith@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'attempts': 2,
            'average_score': 75  # High score
        },
        {
            'student_email': 'mike.wilson@example.com',
            'first_name': 'Mike',
            'last_name': 'Wilson',
            'attempts': 4,
            'average_score': 92  # High score
        },
        {
            'student_email': 'sarah.jones@example.com',
            'first_name': 'Sarah',
            'last_name': 'Jones',
            'attempts': 2,
            'average_score': 45  # Danger zone
        },
        {
            'student_email': 'tom.brown@example.com',
            'first_name': 'Tom',
            'last_name': 'Brown',
            'attempts': 3,
            'average_score': 35  # Danger zone
        }
    ]
    
    # Filter students based on the selected filter
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'high_score':
        filtered_students = [s for s in sample_students if s['average_score'] >= 70]
    elif filter_type == 'danger_zone':
        filtered_students = [s for s in sample_students if s['average_score'] < 50]
    else:
        filtered_students = sample_students
    
    context = {
        'selected_cohort': selected_cohort,
        'filtered_students': filtered_students,
        'filter_type': filter_type,
    }
    return render(request, 'users/teacher_students.html', context)

@login_required
def upload_course(request):
    if not hasattr(request.user, 'teacher_email'):
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('login_teacher')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Course uploaded successfully!')
            return redirect('teacher_home')
    else:
        form = CourseForm()
    return render(request, 'users/upload_course.html', {'form': form})

@login_required
def upload_learning_outcome(request, course_id):
    if not hasattr(request.user, 'teacher_email'):
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('login_teacher')
    
    try:
        course = Course.objects.get(id=course_id, teacher=request.user)
    except Course.DoesNotExist:
        messages.error(request, 'Course not found or access denied.')
        return redirect('teacher_home')
    
    if request.method == 'POST':
        form = LearningOutcomeForm(request.POST, request.FILES)
        if form.is_valid():
            outcome = form.save(commit=False)
            outcome.course = course
            outcome.save()
            messages.success(request, 'Learning outcome uploaded successfully!')
            return redirect('teacher_home')
    else:
        form = LearningOutcomeForm()
    return render(request, 'users/upload_learning_outcome.html', {'form': form, 'course': course})

@login_required
def teacher_courses(request):
    if not hasattr(request.user, 'teacher_email'):
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('login_teacher')
    
    course_form = CourseForm()
    outcome_form = LearningOutcomeForm()
    
    context = {
        'course_form': course_form,
        'outcome_form': outcome_form,
    }
    return render(request, 'users/teacher_courses.html', context)
