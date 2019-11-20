from django.contrib.auth.models import BaseUserManager

# from __future__ import print_function
from django.db import models
from django.db.models import signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

__author__ = 'surendra'

class CustomTestManager(models.Manager):
    def get_queryset(self):
        super_query = super(models.Manager, self).get_queryset()
        print('CustomTestManager is called', super_query)
        return super_query


class UserManager(BaseUserManager):
    def __create_user(self,
                      email,
                      password=None,
                      is_staff=False,
                      is_active=False,
                      is_superuser=False):
        print "/users/managers.py --> __create_user(...)"
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=is_active,
                          is_superuser=is_superuser)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_user(self, email, password):
        # print "/users/managers.py --> create_user(...)"
        return self.__create_user(email,
                                  password,
                                  is_staff=False,
                                  is_active=False,
                                  is_superuser=False)

    def create_superuser(self, email, password):
        # print "/users/managers.py --> create_superuser(...)"
        return self.__create_user(email,
                                  password,
                                  is_staff=True,
                                  is_active=True,
                                  is_superuser=True)

    def create(self, **kwargs):
        # print "/users/managers.py --> create(...)"

        for field in self._meta.concrete_fields:
            if field.is_relation:
                # If the related field isn't cached, then an instance hasn't
                # been assigned and there's no need to worry about this check.
                try:
                    getattr(self, field.get_cache_name())
                except AttributeError:
                    continue
                obj = getattr(self, field.name, None)



        """
        Important to have this to get factories working by default
        """
        return self.create_user(**kwargs)
