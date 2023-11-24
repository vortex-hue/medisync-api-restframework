import base64
import pyotp
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from .Serializers import UserSerializer, UserLoginSerializer, ChangepasswordSerializer, ForgotPasswordSerializer, \
    RecoverPasswordSerializer
import requests


# Create your views here.


class Signup(APIView):

    @staticmethod
    def post(request):
        data = request.data
        serial_obj = UserSerializer(data=data)
        if serial_obj.is_valid(raise_exception=True):
            serial_obj.save()
            return Response({"message": "Successfully signup", "data": serial_obj.data})
        else:
            return Response(serial_obj.errors)


class Login(APIView):

    @staticmethod
    def post(request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(username=data['username'])
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            refresh = str(refresh)
            response = {"username": data['username'], "first_name": user.first_name, "last_name": user.last_name,
                        "id": user.id, "phone": user.phone, "access_token": token,
                        "refresh_token": refresh}
            return Response(response, status=200)
        else:
            return Response(serializer.errors)


class Getaccess(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        response = {
            "msg": "api is accessed by authenticated user"
        }
        return Response(response, status=200)


class ChangePassword(APIView):

    @staticmethod
    def post(request):
        data = request.data
        account = User.objects.get(username=data['username'])
        serial_obj = ChangepasswordSerializer(account, data=data, partial=True)
        if serial_obj.is_valid(raise_exception=True):
            serial_obj.save()
            return Response({"msg": "password updated", "username": data['username'], "password": data['new_password']})
        else:
            return Response(serial_obj.errors)


class DeleteAccount(APIView):
    @staticmethod
    def delete(request):
        query_set = User.objects.all()
        query_set.delete()
        return Response({"msg": "record deleted successfully"})


class ForgotPassword(APIView):
    @staticmethod
    def post(request):
        data = request.data
        serial_obj = ForgotPasswordSerializer(data=data)
        if serial_obj.is_valid(raise_exception=True):
            account = User.objects.get(email=data['email'])
            refresh = RefreshToken.for_user(account)
            token = str(refresh.access_token)
            return Response({"auth_token": token}, status=200)
        else:
            return Response(serial_obj.errors)


class RecoverPassword(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        data = request.data
        serial_obj = RecoverPasswordSerializer(data=data)
        if serial_obj.is_valid(raise_exception=True):
            return Response({"msg": "Account Successfully Updated"})
        else:
            return Response(serial_obj.errors)


class GenerateOTP(APIView):
    @staticmethod
    def get(request, phone):
        if User.objects.filter(phone=phone).exists():
            account = User.objects.get(phone=phone)
            account.counter = account.counter + 1
            account.save()
            unique_value = str(phone) + str(datetime.date(datetime.now()))
            key = base64.b32encode(unique_value.encode())
            otp = pyotp.HOTP(key)
            otp = otp.at(account.counter)
            return Response({"OTP": otp})
        else:
            return Response({"msg": "User not found"})


class VerifyOTP(APIView):
    @staticmethod
    def post(request):
        otp = request.data['OTP']
        if User.objects.filter(phone=request.data['phone']).exists():
            account = User.objects.get(phone=request.data['phone'])
            counter = account.counter
            unique_value = str(request.data['phone']) + str(datetime.date(datetime.now()))
            key = base64.b32encode(unique_value.encode())
            local_otp = pyotp.HOTP(key)
            if local_otp.verify(otp, counter):
                return Response({"msg": "User Verified"})
            else:
                return Response({"msg": "User not Verified"})
        else:
            return Response({"msg": "User not found1"})


class Account(APIView):
    @staticmethod
    def get(request, account_no):
        response = requests.get('http://127.0.0.1:8001/account_details/%s/' % account_no)
        if response.status_code == 404:
            # response.raise_for_status()
            print(response.headers)
            return Response({"msg": "account_not_found"}, status=404)
        else:
            return Response(response.json())

    @staticmethod
    def post(request, account_no):
        # user_name, account_no, phone_no, balance
        data = {'user_name': request.data['user_name'],
                'account_no': request.data['account_no'],
                'phone_no': request.data['phone_no'],
                'balance': request.data['balance']}
        response = requests.post('http://127.0.0.1:8001/accounts/', data=data)
        return Response(response.json())

    @staticmethod
    def delete(request, account_no):
        response = requests.delete('http://127.0.0.1:8001/account_details/%s/' % account_no)
        return Response(response, status=200)


class PasswordChanger(APIView):
    @staticmethod
    def get(request):
        headers = {}
        email = request.query_params['email']
        new_password = request.query_params['new_password']
        response1 = requests.post(url='http://127.0.0.1:8000/forgotpassword/', data={'email': email})
        json_data1 = response1.json()
        print(json_data1['auth_token'])
        token = json_data1['auth_token']
        headers["Authorization"] = f"Bearer {token}"
        response2 = requests.post(url='http://127.0.0.1:8000/recoverpassword/',
                                  data={'email': email, 'new_password': new_password},
                                  headers=headers)
        json_data2 = response2.json()
        print(json_data2)
        return Response(json_data2, status=200)
