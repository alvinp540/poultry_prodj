from django.contrib.auth.backends import BaseBackend
from pouultry_proapp.models import CustomUser

class CustomAuthBackend(BaseBackend):
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate the user based on email and password.
        Return the user object if credentials are correct, else None.
        """
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Retrieve a user object by ID.
        """
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None