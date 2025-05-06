from rest_framework import viewsets, permissions
from .models import Tenant, Organization, Department, Customer
from .serializers import *

# ViewSet for handling CRUD operations
# Serializers for request/response conversion
# Only authenticated users can access

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all() 
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.tenant:
            return Organization.objects.none()
        return Organization.objects.filter(tenant=self.request.tenant)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.tenant:
            return Department.objects.none()
        return Department.objects.filter(organization__tenant=self.request.tenant)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.tenant:
            return Customer.objects.none()
        return Customer.objects.filter(department__organization__tenant=self.request.tenant)