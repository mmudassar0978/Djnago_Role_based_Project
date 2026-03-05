from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login
from .models import User
from .serializers import SignupSerializer, LoginSerializer, EditUserSerializer, AuthTokenObtainPairSerializer
from django.shortcuts import render



class SignupAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer


    def get(self, request, *args, **kwargs):
        return render(request, "signup.html")

    
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"]
        )

        if not user:
            return Response({"detail": "Invalid credentials"}, status=401)
        
        login(request, user)
        redirect_url = "/dashboard/admin/" if user.role == "admin" else "/dashboard/customer/"

        return Response({
            "username": user.username,
            "role": user.role,
            "redirect": redirect_url
        })


class CustomerDashboardAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.role == 'admin':
            return Response({"detail": "Admins cannot access Customer Dashboard"}, status=403)

        context = {
            "username": request.user.username,
            "email": request.user.email,
        }
        return render(request, "customer.html", context)


class AdminDashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request):

        if request.user.role != "admin" and request.user.role != "Admin":
            return Response({"detail": "Access denied"}, status=403)

        users = User.objects.all().order_by("id")
        return render(request, "admin.html", {"users": users})


class AdminDeleteUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        if request.user.role != "admin" and request.user.role != "Admin":
            return Response({"detail": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        if request.user.id == user_id:
            return Response({"detail": "You cannot delete your own account"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_200_OK)


class AdminEditUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_id):
        if request.user.role != "admin":
            return Response({"detail": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        if request.user.id == user_id:
            return Response({"detail": "You cannot edit your own account"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer
