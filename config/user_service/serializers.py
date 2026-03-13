from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, SellerProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['address', 'store_name', 'description', 'created_at']


class BecomeSellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerProfile
        fields = ["store_name", "description"]

        def create(self, validated_data):
            user = self.context["request"].user

            if hasattr(user, "seller_profile"):
                raise serializers.ValidationError(
                    "User is already a seller."
                )

            return SellerProfile.objects.create(
                user=user,
                **validated_data
            )


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

        def validate(self, attrs):
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError("Password do not match")
            return attrs
        
        def create(self, validated_data):
            validated_data.pop('password_confirm')
            user = User.objects.create_user(**validated_data)
            return user
        

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                "Email and password are required."
            )

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )
        
        refresh = RefreshToken.for_user(user)

        attrs["user"] = user
        attrs["access"] = str(refresh.access_token)
        attrs["refresh"] = str(refresh)

        return attrs
    


    