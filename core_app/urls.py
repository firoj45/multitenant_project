from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
