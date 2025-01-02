from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import TenantItemSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django_tenants.utils import schema_context


class ItemListView(generics.ListAPIView):
    """
    API endpoint to retrieve a list of tasks. Filters tasks by assignee if
    'assignee_id' query parameter is provided. Uses Elasticsearch to search
    tasks and retrieves the matching tasks from the database.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TenantItemSerializer

    def get_queryset(self):
        """
        Retrieves the task queryset based on the tenant schema and optional
        'assignee_id'. Searches for tasks in Elasticsearch and fetches the
        corresponding Task objects from the database.
        """
        # Get the host from the request object to extract schema name
        # host = self.request.get_host()
        # schema_name = host.split(".")[0]
        schema_name = self.request.tenant_schema

        # Switch to the correct tenant schema
        with schema_context(schema_name):
            # Start Elasticsearch search for TaskDocument
            return Item.objects.all()


class ItemView(APIView):
    """
    API endpoint to create or update tasks. Handles POST requests to create
    tasks and PUT requests to update existing tasks based on tenant schema.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TenantItemSerializer

    def post(self, request, format=None):
        """
        Creates a new task in the appropriate tenant schema. Returns the
        created task data on success.
        """
        try:
            # Extract schema name from the host
            # host = self.request.get_host()
            # schema_name = host.split(".")[0]
            schema_name = request.tenant_schema

            # Switch to the tenant's schema context
            with schema_context(schema_name):
                # Validate and save the new task
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                # Clean the serialized data to remove empty values
                cleaned_data = {
                    key: value
                    for key, value in serializer.data.items()
                    if value and not isinstance(value, list)
                }
                return Response(
                    {"code": 201, "detail": cleaned_data},
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            # Handle and return any server-side errors
            return Response(
                {"code": 500, "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, format=None):
        """
        Updates an existing task in the appropriate tenant schema. Returns
        the updated task data or a 404 if the task is not found.
        """
        try:
            # Extract schema name from the host and task_id from request
            # host = self.request.get_host()
            item_id = request.data.get("item_id")
            # schema_name = host.split(".")[0]
            schema_name = request.tenant_schema

            # Switch to the tenant's schema context
            with schema_context(schema_name):
                # Find the task by ID
                task_instance = Item.objects.filter(id=item_id).first()

                if task_instance:
                    # Validate and update the task
                    serializer = self.serializer_class(
                        instance=task_instance, data=request.data, partial=True
                    )
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()

                    # Clean the serialized data to remove empty values
                    cleaned_data = {
                        key: value
                        for key, value in serializer.data.items()
                        if value and not isinstance(value, list)
                    }
                    return Response(
                        {"code": 204, "detail": cleaned_data},
                        status=status.HTTP_204_NO_CONTENT,
                    )

                # Return 404 if the task is not found
                return Response(
                    {"code": 404, "detail": "Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as e:
            # Handle and return any server-side errors
            return Response(
                {"code": 500, "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ItemDetailView(APIView):
    """
    API endpoint to retrieve details of a specific task. Handles GET requests
    by returning the task data based on task_id and tenant schema.
    """

    serializer_class = TenantItemSerializer

    def get(self, request):
        """
        Retrieves the task with the given task_id in the appropriate tenant
        schema. Returns the task data or a 404 if the task is not found.
        """
        try:
            # Extract schema name from the host
            # host = self.request.get_host()
            item_id = request.GET.get("item_id")
            # schema_name = host.split(".")[0]
            schema_name = request.tenant_schema

            # Switch to the tenant's schema context
            with schema_context(schema_name):
                # Retrieve the task by ID
                item_instance = Item.objects.filter(id=item_id).first()

                if item_instance is None:
                    # Return 404 if the task is not found
                    return Response(
                        {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
                    )

                # Serialize and return the task data
                serializer = self.serializer_class(item_instance)
                return Response(
                    {"code": 200, "detail": serializer.data}, status=status.HTTP_200_OK
                )

        except Exception as e:
            # Handle and return any server-side errors
            return Response(
                {"code": 500, "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
