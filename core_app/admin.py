from django.contrib import admin
from .models import Tenant, Organization, Department, Customer

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('tenant_id', 'domain')
    search_fields = ('tenant_id', 'domain')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant')
    list_filter = ('tenant',)
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'email')
