from __future__ import unicode_literals

from django.db import models

# Create your models here.
class PersonalLogin(models.Model):
    login_id = models.AutoField(primary_key=True)
    email_id = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'personal_login'


class Container(models.Model):
    container_id = models.AutoField(primary_key=True)
    container_name = models.CharField(max_length=45)
    container_url = models.CharField(max_length=100)
    container_visibility = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'container'