from django.db import models

# Create your models here.
class User(models.Model):
  id = models.AutoField(
    primary_key=True
  )

  user = models.TextField(
    max_length=1000,
    null=False,
    blank=False
  )

  password = models.TextField(
    max_length=1000,
    null=False,
    blank=False
  )

  service = models.TextField(
    max_length=1000,
    default='oauth'
  )

  class Meta:
    db_table = 'User'

class UserLoginHistory(models.Model):
  id = models.AutoField(
    primary_key=True
  )

  user = models.TextField(
    max_length=1000,
    null=False,
    blank=False
  )


  last_login = models.DateTimeField(
    auto_now=True,
    null=False,
    blank=False
  )

  class Meta:
    db_table = 'UserLoginHistory'