from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.contrib.auth.models import User

'''
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='auth_user_groups',
        related_query_name='user',
        )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='auth_user_permissions',
        related_query_name='user',
    )
'''
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address', blank=False, null=False, default='')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
   

    # Add additional fields specific to students here

    def __str__(self):
        return self.user.username


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='recruiter')
    company_email = models.EmailField(max_length=255, unique=False, verbose_name='company email address', blank=False, null=False, default='')
    address = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, unique=False, verbose_name='company name', blank=False, null=False, default='')
    

    # Add additional fields specific to recruiters here

    def __str__(self):
        return self.company_email
    
