from .serializers import EmployeRegisterSerializer, EmployeSerializer, UserRegisterSerialerz
from account.models import User, Employe
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegister(APIView):
    def post(self, request):
        user = UserRegisterSerialerz(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response({'user':user.data})


class RegisterEmploye(APIView):
    def post(self, request, username):
        user = User.objects.get(username=username)
        author = Employe.objects.get(author=user)
        employe = EmployeRegisterSerializer(author, data=request.data)
        employe.is_valid(raise_exception=True)
        employe.save()
        return Response({'employe':employe.data}, status=status.HTTP_200_OK)

 
class GetEmploye(APIView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        serializer = EmployeSerializer(employe)
        return Response(serializer.data)