from django.core.management.base import BaseCommand
from accounts.models import AllowedEmail

class Command(BaseCommand):
    help = "List all AllowedEmail entries in the database"

    def handle(self, *args, **options):
        emails = AllowedEmail.objects.all().order_by("email")
        if not emails.exists():
            self.stdout.write(self.style.WARNING("⚠ No allowed emails in database."))
            return

        self.stdout.write(self.style.MIGRATE_HEADING("\n📋 Current Allowed Emails:"))
        for obj in emails:
            status = "ACTIVE" if obj.active else "INACTIVE"
            self.stdout.write(f"- {obj.email} ({status})")
