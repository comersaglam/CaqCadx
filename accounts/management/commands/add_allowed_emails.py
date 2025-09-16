import json
from django.core.management.base import BaseCommand
from accounts.models import AllowedEmail

class Command(BaseCommand):
    help = "Add emails from allowed_emails.json"

    def handle(self, *args, **options):
        with open("accounts/management/commands/allowed_emails.json", "r") as f:
            data = json.load(f)

        add_list = data.get("add", [])
        created_count = 0

        for email in add_list:
            obj, created = AllowedEmail.objects.get_or_create(
                email=email.lower().strip(),
                defaults={"active": True},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Added: {email}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Already exists: {email}"))

        self.stdout.write(self.style.SUCCESS(f"\n✔ {created_count} new emails added."))
