from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentLoginForm, TeacherRegistrationForm, TeacherLoginForm

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
            teacher_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(teacher_email=teacher_email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('teacher_home')
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
    return render(request, 'users/teacher_home.html')
