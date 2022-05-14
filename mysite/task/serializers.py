from rest_framework import serializers

from .models import Task
from account.serializers import EmployeSerializer

class TaskSerializers(serializers.ModelSerializer):
    employe = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'creator', 'employe']

    def get_employe(self, obj):
        employe = obj.employe
        serializer = EmployeSerializer(employe, many=False)
        return serializer.data
