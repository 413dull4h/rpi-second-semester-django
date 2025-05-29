from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentication backend that allows users to log in with either username or email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find a user matching either username or email
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # No user found with the provided username/email
            return None
        except User.MultipleObjectsReturned:
            # Multiple users found (should not happen if email is unique)
            # Return the first one that matches
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
            if user and user.check_password(password):
                return user
        return None