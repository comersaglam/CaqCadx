from django.conf import settings
from .models import AllowedEmail

def email_is_allowed(email: str) -> bool:
    if not email:
        return False

    email = email.lower().strip()
    domain = email.split("@")[-1]

    # Domain check
    domains = getattr(settings, "ALLOWED_EMAIL_DOMAINS", set())
    domain_ok = not domains or domain in {d.lower() for d in domains}

    # Specific email check
    email_ok = AllowedEmail.objects.filter(email__iexact=email, active=True).exists()

    # ✅ Require both domain AND email approval
    return domain_ok and email_ok
