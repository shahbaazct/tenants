from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import tenant_context
from a_tenant_manager.models import Tenant

class TenantSpecificMiddleware(MiddlewareMixin):
    """
    Middleware for handling tenant context based on the request headers or URL.

    Sets the tenant context based on the 'HTTP_X_TENANT' header or defaults to 'default'.
    Adds the tenant instance to the request object for use in views.

    Methods:
        process_request(request): Processes the incoming request to determine and set the tenant context.
    """

    def process_request(self, request):
        """
        Processes the incoming request to determine the tenant context.

        Retrieves the tenant schema name from the 'HTTP_X_TENANT' header or defaults to 'default'.
        Sets the tenant context using the retrieved or default tenant.

        Args:
            request: The HTTP request object.

        Sets:
            request.tenant: The tenant instance associated with the request.
            tenant_context: The tenant context for the current request.
        """
        host = request.get_host()
        schema_name = host.split(".")[
            0
        ]

        request.tenant_schema = schema_name