from decimal import Clamped
from statistics import mode
from rest_framework import serializers
from .models import MultiEmail, UserReg, Verification_Otp
from random import randint
import string
from django.core.mail import send_mail



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = UserReg
        fields = '__all__'

    def validate_email(self, data):
        obj = UserReg.objects.filter(email=data)
        if obj:
            raise serializers.ValidationError('email must be unique')
        return data

    def validate(self, attrs):
        if "username" in attrs:
            if " " in attrs['username']:
                raise serializers.ValidationError("username must not contain special characters except '.','_'")
            for i in string.punctuation:
                if (i != ".") and (i != "_"):
                    if i in attrs['username']:
                        raise serializers.ValidationError("username must not contain special characters except '.','_'")
        return attrs

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification_Otp
        fields = '__all__'

class UpdateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiEmail
        fields = '__all__'