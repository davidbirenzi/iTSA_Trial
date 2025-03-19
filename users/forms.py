from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import StudentUser, TeacherUser, Course, LearningOutcome

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
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Teacher Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Teacher Email'
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if email and password:
            try:
                user = TeacherUser.objects.get(teacher_email=email)
                if not user.check_password(password):
                    raise forms.ValidationError('Invalid email or password.')
            except TeacherUser.DoesNotExist:
                raise forms.ValidationError('Invalid email or password.')
        
        return cleaned_data

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'faculty', 'course_file']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class LearningOutcomeForm(forms.ModelForm):
    class Meta:
        model = LearningOutcome
        fields = ['title', 'description', 'outcome_file']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 