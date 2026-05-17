import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import UserSerializer

logger = logging.getLogger(__name__)


class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })

        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class AddToGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, type_name):
        # Check group exists
        pokemon_type = Group.objects.filter(name=type_name).first()
        if pokemon_type is None:
            return Response(
                {"error": f"Group {type_name} Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Add user to group/pokemon type
        request.user.groups.add(pokemon_type)
        logger.info(f"user {request.user.username} added to group {type_name}")

        return Response(UserSerializer(request.user).data)


class RemoveFromGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, type_name):
        pokemon_type = Group.objects.filter(name=type_name).first()
        if pokemon_type is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Remove from group
        request.user.groups.remove(pokemon_type)
        logger.info(f"user {request.user.username} removed from group {type_name}")

        return Response(status=status.HTTP_204_NO_CONTENT)
