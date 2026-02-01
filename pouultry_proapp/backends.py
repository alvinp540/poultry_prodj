from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from pouultry_proapp.models import CustomUser

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with email
    """
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        """
        Authenticate user using email and password
        """
        # Allow authentication with either username or email parameter
        email = email or username
        
        if email is None or password is None:
            return None
        
        try:
            # Get user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce timing
            # difference between existing and non-existing users
            User().set_password(password)
            return None
        
        # Check if password is correct
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None

    def get_user(self, user_id):
        """
        Retrieve a user object by ID.
        """
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None