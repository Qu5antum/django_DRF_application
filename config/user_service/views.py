from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, SellerProfileSerializer, BecomeSellerSerializer
from .models import User, SellerProfile

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()   
    serializer_class = UserRegisterSerializer
    permission_classes = []
    

class UserLoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(
            data = request.data,
            context = {"request": request}
        )

        serializer.is_valid(raise_exception=True)

        return Response({
            "access": serializer.validated_data["access"],
            "refresh": serializer.validated_data["refresh"],
            "email": serializer.validated_data["user"].email
        }, status=status.HTTP_200_OK)
    

class BecomeSellerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BecomeSellerSerializer(
            data=request.data,
            context = {"request", request}
        )

        serializer.is_valid(raise_exception=True)

        seller = serializer.save()

        return Response({
            "store_name": seller.store_name,
            "message": "Seller profile created"
        }, status=status.HTTP_201_CREATED)

    



