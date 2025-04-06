from django.core.management import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        if CustomUser.objects.filter(phone='79999999999').exists():
            self.stdout.write(self.style.SUCCESS('Success create superuser'))
        else:
            user = CustomUser.objects.create_user(username="baseuser", password="baseuser")
            user.phone = '79999999999'
            user.save()
            self.stdout.write(self.style.SUCCESS('Success create superuser'))
