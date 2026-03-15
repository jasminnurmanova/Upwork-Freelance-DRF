from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (SignUpSerializer,LoginSerializer, ProfileUpdateSerializer, ChangePasswordSerializer)


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Account yaratildi",
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Tizimga muvaffaqiyatli kirdingiz"
            },
            status=status.HTTP_200_OK
        )

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            raise ValidationError({"refresh": "Refresh token yuborilmadi"})
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            raise ValidationError({"refresh": "Token noto'g'ri"})

        return Response(
            {
                "message": "Tizimdan chiqdingiz"
            },
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user

        data = {
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "bio": user.bio,
            "avatar": user.avatar.url if user.avatar else None,
            "created_at": user.created_at
        }
        return Response(data, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request):
        serializer = ProfileUpdateSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Profil yangilandi",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class AvatarUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request):
        user = request.user
        avatar = request.FILES.get("avatar")
        if not avatar:
            raise ValidationError({"avatar": "Rasm yuklanmadi"})
        user.avatar = avatar
        user.save()
        return Response(
            {"message": "Avatar yangilandi"},
            status=status.HTTP_200_OK
        )

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Parol yangilandi"
            },
            status=status.HTTP_200_OK)

