from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model

from a_tenant_manager.serializers import TenantUserSerializer


class TenantListView(generics.ListAPIView):
    pass


class TenantLoginView(APIView):
    """Handle login requests for tenants.

    This view authenticates the user based on the provided username and password,
    and generates JWT tokens for successful authentication.
    """

    def post(self, request):
        # import pdb;pdb.set_trace()
        # Extract host, username, and password from the request
        # host = self.request.get_host()
        username = request.data.get("username")
        password = request.data.get("password")
        # schema_name = host.split(".")[
        #     0
        # ]  # Assume schema name is derived from the subdomain

        schema_name = request.tenant_schema

        # Validate input
        if not schema_name or not username or not password:
            return Response(
                {
                    "code": 400,
                    "detail": "Schema name, username, and password are required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Authenticate the user within the tenant's schema
            with schema_context(schema_name):
                user = authenticate(username=username, password=password)
                if user is None:
                    return Response(
                        {"code": 401, "detail": "Invalid credentials."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                # Generate JWT tokens for the authenticated user
                refresh = RefreshToken.for_user(user)
                data = {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "is_active": user.is_active,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }

                return Response(
                    {"code": 200, "detail": data}, status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {"code": 500, "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
