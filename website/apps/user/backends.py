from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # check if the user is trying to login with their phone number
            user = UserModel.objects.get(phone=username)
        except UserModel.DoesNotExist:
            # if the user doesn't exist, then try with their email
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None