from account.api.permissions import *
from .serializers import *
from account.models import User, Employe, Worker, Director, Admin, Deputy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
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


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class DirectorProfile(APIView):
    permission_classes = [IsDirector]

    def get(self, request):

        director = Director.objects.get(id=request.user.id)
        serializer = DirectorProfileSerializer(director, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

api_view(['GET'])
permission_classes([IsWorker])
def worker_profile(self, request):
    worker = Worker.objects.get(id=request.user.id)
    serializer = WorkerProfileSerializer(worker, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


class WorkerProfile(APIView):
    permission_classes = [IsWorker]

    def get(self, request):
        worker = Worker.objects.get(id=request.user.id)
        serializer = WorkerProfileSerializer(worker, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
