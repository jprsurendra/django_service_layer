# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils import timezone


from .managers import UserManager, CustomTestManager


class BaseUser(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def save(self, *args, **kwargs):
        print "/users/models.py --> class BaseUser --> save(...)"
        self.full_clean()
        # super().save(*args, **kwargs)
        super(BaseUser, self).save(*args, **kwargs)

    def get_full_name(self):
        print "/users/models.py --> class BaseUser --> get_full_name(...)"
        return self.profile.full_name

    def get_short_name(self):
        print "/users/models.py --> class BaseUser --> get_short_name(...)"
        return self.get_full_name()

    def get_description(self):
        print "/users/models.py --> class BaseUser --> get_description(...)"
        return self.profile.description

    @property
    def name(self):
        print "/users/models.py --> class BaseUser --> name(...)"
        return self.get_full_name()

    def __str__(self):
        print "/users/models.py --> class BaseUser --> __str__(...)"
        return 'BaseUser(name=' + self.email + ')'
        # return f'{self.email}'




class TestModel(models.Model):
    name = models.CharField(max_length=100, default='--')
    password = models.CharField(max_length=100, default='--')
    # auto_fill_field = models.CharField(max_length=100)

    objects = CustomTestManager()

    class Meta:
        db_table = 'tbl_test_model'

    def __unicode__(self):
        return '%s' % (self.name)

    def save(self, *args, **kwargs):
        print('save() is called.')
        super(TestModel, self).save(*args, **kwargs)

    # def json_equivalent(self):
    #     dictionary = {}
    #     for field in self._meta.get_all_field_names():
    #         dictionary[field] = self.__getattribute__(field)
    #     return dictionary
    #
    # def json(self):
    #     return {
    #         'id': self.pk,
    #         'name': self.name,
    #         'password': self.password,
    #     }

    # def save(self):
    #     if not self.pk :
    #        ### we have a newly created object, as the db id is not set
    #        self.date_created = datetime.datetime.now()
    #     super(myModel , self).save()