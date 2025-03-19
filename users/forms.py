from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import StudentUser, TeacherUser

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = StudentUser
        fields = ('first_name', 'last_name', 'student_email', 'faculty', 'academic_year', 'trimester', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['student_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['faculty'].widget.attrs.update({'class': 'form-control'})
        self.fields['academic_year'].widget.attrs.update({'class': 'form-control'})
        self.fields['trimester'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class StudentLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = StudentUser
        fields = ('student_email', 'password')

class TeacherRegistrationForm(UserCreationForm):
    class Meta:
        model = TeacherUser
        fields = ('first_name', 'last_name', 'teacher_email', 'faculty', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['teacher_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['faculty'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class TeacherLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = TeacherUser
        fields = ('teacher_email', 'password') 