from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentUser, TeacherUser

class StudentUserAdmin(UserAdmin):
    model = StudentUser
    list_display = ('student_email', 'first_name', 'last_name', 'faculty', 'academic_year', 'trimester', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'faculty', 'academic_year', 'trimester')
    fieldsets = (
        (None, {'fields': ('student_email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'faculty', 'academic_year', 'trimester')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student_email', 'first_name', 'last_name', 'faculty', 'academic_year', 'trimester', 'password1', 'password2'),
        }),
    )
    search_fields = ('student_email', 'first_name', 'last_name', 'faculty')
    ordering = ('student_email',)

class TeacherUserAdmin(UserAdmin):
    model = TeacherUser
    list_display = ('teacher_email', 'first_name', 'last_name', 'faculty', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'faculty')
    fieldsets = (
        (None, {'fields': ('teacher_email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'faculty')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('teacher_email', 'first_name', 'last_name', 'faculty', 'password1', 'password2'),
        }),
    )
    search_fields = ('teacher_email', 'first_name', 'last_name', 'faculty')
    ordering = ('teacher_email',)

admin.site.register(StudentUser, StudentUserAdmin)
admin.site.register(TeacherUser, TeacherUserAdmin)
