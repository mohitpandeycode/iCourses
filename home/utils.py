from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from .models import UserProfile
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        try:
            user_profile = UserProfile.objects.get(user=user)
            is_email_verified = user_profile.is_email_varified
        except UserProfile.DoesNotExist:
            is_email_verified = False
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(is_email_verified))


generate_token = TokenGenerator()
