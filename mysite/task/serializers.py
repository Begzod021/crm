from urllib import request
from xml.dom import UserDataHandler
from account.models import User, Employe
from rest_framework import serializers

class EmployeSerialerz(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = ['user']
    def get_user(self, request):
        user = User.objects.get(username=request.user.username)
        employe = Employe.objects.get(user=user)
        return employe