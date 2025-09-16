from django.core.exceptions import PermissionDenied
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import AllowedEmail
from django.contrib import messages

def email_is_allowed(email: str) -> bool:
    if not email:
        return False
    return AllowedEmail.objects.filter(email__iexact=email, active=True).exists()

class AccountAdapter(DefaultAccountAdapter):
    # Blocks regular (username/password) signup if email not allowed
    def is_open_for_signup(self, request):
        # Let allauth create the form first; we enforce in clean_email too
        return True

    def clean_email(self, email):
        email = super().clean_email(email)
        if not email_is_allowed(email):
            raise PermissionDenied("This email is not authorized to register.")
        return email
    
class SocialAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email") or sociallogin.user.email
        # Your custom email check
        from .utils import email_is_allowed
        return email_is_allowed(email)

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        # Just show a message and raise PermissionDenied
        messages.error(request, "❌ Your email is not authorized for access.")
        raise PermissionDenied("Unauthorized email.")
