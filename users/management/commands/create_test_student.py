from django.core.management.base import BaseCommand
from users.models import StudentUser

class Command(BaseCommand):
    help = 'Creates a test student user'

    def handle(self, *args, **kwargs):
        try:
            student = StudentUser.objects.create_user(
                student_email='test@student.com',
                password='test123',
                first_name='Test',
                last_name='Student',
                faculty='IT',
                academic_year=2024,
                trimester=1
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created student user: {student.student_email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating student user: {str(e)}')) 