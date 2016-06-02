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


