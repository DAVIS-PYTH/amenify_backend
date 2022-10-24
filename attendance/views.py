from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Authentication Imports
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status

from django.contrib.auth.hashers import make_password, check_password

from .models import Attendance

from .serializers import AttendanceSerializer, UserSerializerWithToken

# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user, many=False).data
        for key, value in serializer.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# REGISTRATION VIEW
@api_view(["POST"])
def registerUser(request):
    data = request.data
    
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {"detail": "User with this Email already exist"}
        return Response(message, status=status.HTTP_403_FORBIDDEN)


# Get user attendance list
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAttendanceList(request):
    user = request.user
    attendanceList = Attendance.objects.filter(user=user)
    serializer = AttendanceSerializer(attendanceList, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# update user attendance list
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def updateAttendanceList(request):
    user = request.user
    
    data = request.data
    
    attendance = Attendance.objects.get(uuid=data['Id'])
    
    if attendance.user != user:
        message = {"detail": "You are not allowed to this!"}
        return Response(message, status=status.HTTP_403_FORBIDDEN)

    
    attendance.Subject = data['Subject']
    attendance.save()
    
    attendanceList = Attendance.objects.filter(user=user)
    serializer = AttendanceSerializer(attendanceList, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# add user attendance
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addAttendance(request):
    user = request.user
    
    data = request.data
    
    attendance = Attendance.objects.create(
        user=user,
        uuid=data['Id'],
        Subject=data['Subject'],
        StartTime=data['StartTime'],
        EndTime=data['EndTime']
        )
    
    attendance.save()
    
    attendanceList = Attendance.objects.filter(user=user)
    serializer = AttendanceSerializer(attendanceList, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
