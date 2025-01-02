from django.contrib import admin
from .models import *

# Register your models here.


class TenantAdminSite(admin.AdminSite):
    def __init__(self, name=...):
        super().__init__(name)
        self.register(Tenant)
        self.register(Domain)


tenant_admin_site = TenantAdminSite(name="tenant_admin_site")
