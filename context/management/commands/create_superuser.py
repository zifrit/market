from django.core.management import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        if CustomUser.objects.filter(username='admin', is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Success create superuser'))
        else:
            CustomUser.objects.create_superuser(username="admin", password="admin")
            self.stdout.write(self.style.SUCCESS('Success create superuser'))
