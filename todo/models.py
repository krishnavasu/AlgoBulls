from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
# Create your models here.


    

class User(AbstractBaseUser):
    name = models.CharField(max_length=30,null=False,blank=False)
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    # history = models.ManyToManyField(,blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name
    
   

class Todo(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('WORKING', 'Working'),
        ('DONE', 'Done'),
        ('OVERDUE', 'Overdue'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    title = models.CharField(max_length=100,)
    description = models.CharField(max_length=1000,)
    due_date = models.DateField(blank=True, null=True,)
    tags = models.ManyToManyField('Tag', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

class Tag(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name