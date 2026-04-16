from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class Command(BaseCommand):
    help = 'Create API user and tokens'

    def handle(self, *Args, **kwargs):
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@luxurycars.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            Token.objects.create(user=admin)
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'user@luxurycars.com'}
        ) 
        if created:
            user.set_password('test123')
            user.save()
            Token.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS('Created test user'))   