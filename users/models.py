from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class StudentUserManager(BaseUserManager):
    def create_user(self, student_email, password=None, **extra_fields):
        if not student_email:
            raise ValueError('The Student Email field must be set')
        email = self.normalize_email(student_email)
        user = self.model(student_email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('faculty', 'Admin')
        extra_fields.setdefault('academic_year', 1)
        extra_fields.setdefault('trimester', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(student_email, password, **extra_fields)

class TeacherUserManager(BaseUserManager):
    def create_user(self, teacher_email, password=None, **extra_fields):
        if not teacher_email:
            raise ValueError('The Teacher Email field must be set')
        email = self.normalize_email(teacher_email)
        user = self.model(teacher_email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, teacher_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('faculty', 'Admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(teacher_email, password, **extra_fields)

class StudentUser(AbstractUser):
    # Remove username field since we'll use email for authentication
    username = None
    
    # Add custom fields
    student_email = models.EmailField(unique=True)
    faculty = models.CharField(max_length=100)
    academic_year = models.IntegerField()
    trimester = models.IntegerField()
    
    # Set email field as the username field
    USERNAME_FIELD = 'student_email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'faculty', 'academic_year', 'trimester']
    
    objects = StudentUserManager()
    
    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_email})"

class TeacherUser(AbstractUser):
    username = None
    teacher_email = models.EmailField(unique=True)
    faculty = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'teacher_email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'faculty']
    
    objects = TeacherUserManager()
    
    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='teacher_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='teacher_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_email})"
