from wsgiref import validate
from xml.dom import UserDataHandler
from .models import User, Employe
from rest_framework import serializers


class UserRegisterSerialerz(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username','password', 'password2')


    def create(self, validated_data):
        password = validated_data['password']
        password2 = validated_data['password2']
        print(password)
        if password == password2:
            print(password)
            user = User.objects.create(
                username=validated_data['username'],
                password = password,
            )
            user.save()


            return user
        return None

class EmployeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class EmployeSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Employe
        fields = '__all__'