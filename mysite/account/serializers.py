from turtle import position
from wsgiref import validate
from xml.dom import UserDataHandler
from .models import Postion, Section, User, Employe
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

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postion
        fields = ['position']

    
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['name']



class EmployeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    position = serializers.SerializerMethodField(read_only=True)
    section = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Employe
        fields = '__all__'
    
    def get_user(self, obj):
        user = obj.user

        serializer_user = UserSerializer(user, many=False)
        
        return serializer_user.data
    

    def get_position(self, obj):
        position = obj.position

        serializer_position = PositionSerializer(position, many=False)

        return serializer_position.data

    def get_section(self, obj):
        section = obj.section

        serializer_section = SectionSerializer(section, many=False)
        return serializer_section.data
    