from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
            
        try:
            # Case-insensitive search for username or email
            # Normalize the email by lowercasing it
            if '@' in username:
                username_lookup = username.lower()  # Normalize email to lowercase
                user = User.objects.get(Q(email__iexact=username_lookup))
            else:
                user = User.objects.get(Q(username__iexact=username))
                
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # If no exact match was found, try a more general search
            try:
                user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
                if user.check_password(password):
                    return user
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user.
                User().set_password(password)
                
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
