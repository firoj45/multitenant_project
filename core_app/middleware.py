from .models import Tenant
from django.utils.deprecation import MiddlewareMixin

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domain = request.headers.get('X-Tenant-Domain')
        if domain:
            try:
                request.tenant = Tenant.objects.get(domain=domain)
            except Tenant.DoesNotExist:
                request.tenant = None
        else:
            request.tenant = None
