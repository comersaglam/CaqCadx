import json
from django.core.management.base import BaseCommand
from accounts.models import AllowedEmail

class Command(BaseCommand):
    help = "Delete emails from allowed_emails.json"

    def handle(self, *args, **options):
        with open("accounts/management/commands/allowed_emails.json", "r") as f:
            data = json.load(f)

        delete_list = data.get("delete", [])
        deleted_count = 0

        for email in delete_list:
            try:
                obj = AllowedEmail.objects.get(email__iexact=email.strip())
                obj.delete()
                deleted_count += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Deleted: {email}"))
            except AllowedEmail.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠ Not found, cannot delete: {email}"))

        self.stdout.write(self.style.SUCCESS(f"\n✔ {deleted_count} emails deleted."))
