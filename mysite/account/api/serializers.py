from account.models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from account.models import Director

class UserRegisterSerialerz(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username','password', 'password2', 'role', 'approve')


    def create(self, validated_data):
        password = validated_data['password']
        password2 = validated_data['password2']
        print(password)
        if validated_data['role'] == 'admin':
            validated_data['is_staff'] = True
        else:
            validated_data['is_staff'] = False
        if password == password2:
            print(password)
            user = User.objects.create(
                username=validated_data['username'],
                role = validated_data['role'],
                is_staff = validated_data['is_staff'],
                approve = True
            )
            user.set_password(password)
            user.save()


            return user
        return None

class DirectorProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Director
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login']


class WorkerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login']

class DeputyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deputy
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login']

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True,required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User

        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'Password fields didnt match'})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError({'old_password':'Old password is not correct'})

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance

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
    