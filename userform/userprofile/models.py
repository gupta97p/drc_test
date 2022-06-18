from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class user_reg(AbstractUser):
    username = models.CharField(max_length=20, unique=True, blank=False)
    mobile = models.CharField(max_length=10, blank=True, null=True, unique=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    gender = models.CharField(max_length=8, default='Male')
    mobile = models.PositiveBigIntegerField(blank=False)

    def __str__(self):
        return self.username

class Verification_Otp(models.Model):
    user = models.ForeignKey(user_reg, on_delete=models.CASCADE, null=False)
    expired = models.CharField(max_length=10, null=True)
    pending = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField()
    attempts = models.IntegerField(default=0, blank=False)