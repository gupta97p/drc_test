from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserReg(AbstractUser):
    username = models.CharField(max_length=20, unique=True, blank=False)
    mobile = models.CharField(max_length=10, blank=True, null=True, unique=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    gender = models.CharField(max_length=8, default='Male')
    mobile = models.PositiveBigIntegerField(null=True)

    def __str__(self):
        return self.username

class Verification_Otp(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE, null=False)
    expired = models.CharField(max_length=10, null=True)
    pending = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField()
    attempts = models.IntegerField(default=0, blank=False)
    last_attempt = models.DateTimeField(null=True)

class MultiEmail(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    email_id = models.EmailField()
    is_primary = models.BooleanField(default=False)