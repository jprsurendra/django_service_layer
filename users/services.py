from rest_framework.exceptions import ValidationError

from .models import BaseUser


# def create_user(*, email: str, password: str) -> BaseUser:
def create_user(email, password):
    print "/users/services.py --> save(...)"
    return BaseUser.objects.create(email=email, password=password)

create_user.__annotations__ = {'email': str, 'password': str, 'return': BaseUser}

