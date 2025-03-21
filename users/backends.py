from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import TeacherUser, StudentUser

class StudentAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = StudentUser.objects.get(student_email=username)
            if user.check_password(password):
                return user
        except StudentUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return StudentUser.objects.get(pk=user_id)
        except StudentUser.DoesNotExist:
            return None

class TeacherAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = TeacherUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except TeacherUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return TeacherUser.objects.get(pk=user_id)
        except TeacherUser.DoesNotExist:
            return None 