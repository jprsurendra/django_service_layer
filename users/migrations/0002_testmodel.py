# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-16 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='--', max_length=100)),
                ('password', models.CharField(default='--', max_length=100)),
            ],
            options={
                'db_table': 'tbl_test_model',
            },
        ),
    ]
