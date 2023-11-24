from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate, password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'phone')

    @staticmethod
    def validate_password(data):
        password_validation.validate_password(password=data, user=User)
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data['first_name'] == data['last_name']:
            raise serializers.ValidationError("FirstName and LastName cannot be same!")
        else:
            return data


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            return data
        else:
            raise serializers.ValidationError("User Not Authenticated!")


class GetuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ChangepasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'new_password']

    @staticmethod
    def validate_new_password(data):
        password_validation.validate_password(user=User, password=data)
        return data

    def validate(self, data):
        if data['password'] == data['new_password']:
            raise serializers.ValidationError("New Password is Matching Old Password!")
        else:
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                return data
            else:
                raise serializers.ValidationError("Authentication Failed")

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=30, required=True)

    def validate(self, data):
        email = data['email']
        if User.objects.filter(email=email).exists():
            return data
        else:
            raise serializers.ValidationError("Account not Exists")


class RecoverPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=30)
    new_password = serializers.CharField(max_length=30)

    def validate(self, data):
        email = data['email']
        new_password = data['new_password']
        if User.objects.filter(email=email).exists():
            if len(new_password) < 8:
                raise serializers.ValidationError("password must have at least 8 char")
            else:
                account = User.objects.get(email=email)
                account.set_password(new_password)
                account.save()
                return data
        else:
            raise serializers.ValidationError("Account not found")
