from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import UserReg, Verification_Otp
from .serializers import *

def authenticate_user(email, password):
    try:
        user = UserReg.objects.get(email=email)
    except UserReg.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
        return None


class LoginViewSet(ViewSet):
    def create(self, request):
        try:
            user_obj = UserReg.objects.filter(mobile=request.POST.get('mobile')).first()
            if not user_obj:
                return Response({'message': 'invalid mobile number'}, 401)
            otp = randint(100000, 1000000)
            print("otp for user is ", otp)
            otp_dict = {'user': user_obj.id, 'pending': otp, 'created_at': datetime.now()}
            otpdata = OtpSerializer(data=otp_dict)
            if not otpdata.is_valid():
                return Response({"message":otpdata.errors}, 422)
            otpdata.save()
            return Response({'message': "Otp sent to the registered mobile number"}, 200)
        except Exception as e:
            return Response({"status": "failed", 'message': str(e)}, 500)

    def otp(self, request, pk=None):
        try:
            user_obj = UserReg.objects.filter(mobile=pk).first()
            print(pk, user_obj)
            otp_obj = Verification_Otp.objects.filter(user=user_obj.id).first()
            if otp_obj.attempts >= 3 and(otp_obj.last_attempt + timedelta(minutes=5)) > datetime.now():
                return Response({'message': 'Max number of retries reached. Please wait for 5 minutes and then try again'}, 401)
            if not otp_obj.pending == request.POST.get('otp'):
                otp_obj.attempts += 1
                otp_obj.last_attempt = datetime.now()
                otp_obj.save()
                return Response({'message': 'Invalid OTP'}, 401)
            return Response({'message':'Otp Verified Successfully.'})
        except Exception as e:
            return Response("some error occurred " + str(e), 422)


class RegisterViewSet(ViewSet):
    # create user
    def create(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"status": "failed", 'message': serializer.errors}, 422)
            serializer.save()
            print(f"Welcome {serializer.data['username']}")
            user_detail = MultiEmail.objects.filter(pk=serializer.data['id']).first()
            print(type(request.data))
            user_dict = {'email_id':serializer.data['email'], 'user':serializer.data['id'], 'is_primary':True}
            serializer = UpdateEmailSerializer(user_detail, data=user_dict, partial=True)
            if not serializer.is_valid():
                return Response({"status": "failed", 'data': serializer.errors}, 422)
            serializer.save()
            return Response({'message': 'record Saved successfully', 'data': serializer.data}, 200)
        except Exception as e:
            return Response({"status": "failed", 'message': str(e)}, 500)
    
    def partial_update(self, request, pk=None):
        try:
            # token = Token.objects.get(key=(request.META.get('HTTP_AUTHORIZATION'))[6:]).user
            user_detail = MultiEmail.objects.filter(pk=pk).first()
            serializer = UpdateEmailSerializer(user_detail, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({"status": "failed", 'data': serializer.errors}, 422)
            serializer.save()
        except Exception as e:
            return Response('some exception occurred' + str(e), 500)
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        try:
            user_detail = UserReg.objects.get(pk=pk)
            user_detail.delete()
        except Exception as e:
            return Response('some exception occurred ' + str(e), 500)
        return Response('record Deleted successfully')