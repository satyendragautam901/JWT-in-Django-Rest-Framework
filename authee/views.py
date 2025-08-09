# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .serializers import StudentModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .customThrottle import MyThrottle # this is custom throttle
from rest_framework.throttling import ScopedRateThrottle # this used to apply for some of part

# Create your views here.
class StudentViewset(viewsets.ViewSet):
   # scope rate throttle used for only some part eg: listview, createview etc
     
    authentication_classes = [JWTAuthentication] # this is token authentication
    permission_classes = [IsAuthenticatedOrReadOnly] 
    throttle_classes = [UserRateThrottle, AnonRateThrottle] # anonymous user 
    # throttle_classes = [UserRateThrottle, MyThrottle] # anonymous user can throttle by custom throttle

    def list(self, request):
        stu = Student.objects.all()

        serializer = StudentModelSerializer(stu, many = True)

        return Response({
            "status":True,
            "message":"All student record fetched ",
            "data":serializer.data
        },status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        try:
            stu = Student.objects.get(id = pk)

        except Student.DoesNotExist:
            return Response({
            "status":False,
            "message": f"No data found with this id {pk}",
            
        },status=status.HTTP_404_NOT_FOUND)

        serializer = StudentModelSerializer(stu)
        
        return Response({
            "status":True,
            "message":"Student record fetched ",
            "data":serializer.data
        },status=status.HTTP_200_OK)
    
    def create(self, request):
        print("requested data ", request.data)
        serializer = StudentModelSerializer(data = request.data)

        if(serializer.is_valid()):
            serializer.save()

            return Response({
            "status":True,
            "message":"student record created successfully ",
            "data":serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response({
            "status":False,
            "message":"Error during creating record ",
            "data":serializer.data
        },status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):

        try:
            stu = Student.objects.get(id = pk)

        except Student.DoesNotExist:
            return Response({
            "status":False,
            "message": f"No data found with this id {pk}",
            
        },status=status.HTTP_404_NOT_FOUND)

        serializer = StudentModelSerializer(stu, data = request.data, partial = True)

        if(serializer.is_valid()):
            serializer.save()
            return Response({
            "status":True,
            "message":"student record updated successfully ",
            "data":serializer.data
            },status=status.HTTP_200_OK)
        
        return Response({
            "status":False,
            "message":"Error during updating data . ",
            "data":serializer.data
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self,request, pk):
        try:
            stu = Student.objects.get(id = pk)

        except Student.DoesNotExist:
            return Response({
            "status":False,
            "message": f"No data found with this id {pk}",
            
        },status=status.HTTP_404_NOT_FOUND)

        serializer = StudentModelSerializer(stu)

        stu.delete()

        return Response({
            "status":True,
            "message":"student record deleted successfully ",
            "data":serializer.data
            },status=status.HTTP_204_NO_CONTENT)