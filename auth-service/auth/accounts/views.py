from rest_framework import generics, permissions
from .models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PatientProfile, DoctorProfile, PharmacistProfile
from .serializers import (
    PatientProfileSerializer, DoctorProfileSerializer, PharmacistProfileSerializer, UserProfileSerializer
)
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CreateProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        role = user.role

        if role == 'patient':
            if hasattr(user, 'patient_profile'):
                return Response({'error': 'Patient profile already exists'}, status=400)
            serializer = PatientProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        elif role == 'doctor':
            if hasattr(user, 'doctor_profile'):
                return Response({'error': 'Doctor profile already exists'}, status=400)
            serializer = DoctorProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        elif role == 'pharmacist':
            if hasattr(user, 'pharmacist_profile'):
                return Response({'error': 'Pharmacist profile already exists'}, status=400)
            serializer = PharmacistProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        return Response({'error': 'Invalid role'}, status=400)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

class CheckRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        roles = request.data.get("roles", [])

        if not isinstance(roles, list):
            return Response({"error": "roles must be a list"}, status=400)

        is_allowed = user.role in roles
        return Response({
            "user_id": user.id,
            "role": user.role,
            "allowed": is_allowed
        })
        
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # có thể check thêm admin

    def perform_create(self, serializer):
        user = serializer.save()
        # Nếu profile được gửi cùng, sẽ được xử lý trong serializer.update()

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Có thể thêm kiểm tra admin
    lookup_field = 'id'
    
class UserListByRoleView(APIView):
    def get(self, request, role):
        if role not in ['patient', 'doctor', 'pharmacist']:
            return Response({'detail': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        users = User.objects.filter(role=role)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)