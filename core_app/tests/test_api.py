from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core_app.models import Tenant, Organization, Department, Customer


class MultiTenantAPITest(APITestCase):
    def setUp(self):
        # Create two tenants
        self.tenant1 = Tenant.objects.create(tenant_id='tenant1', domain='tenant1.com')
        self.tenant2 = Tenant.objects.create(tenant_id='tenant2', domain='tenant2.com')

        # Create user and token
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            HTTP_X_TENANT_DOMAIN='tenant1.com'
        )

    def test_organization_crud_and_tenant_isolation(self):
        # Create organization in tenant1
        org_data = {'name': 'Org A', 'tenant': self.tenant1.id}
        response = self.client.post('/api/organizations/', org_data, format='json')
        self.assertEqual(response.status_code, 201)
        org_id = response.data['id']

        # Confirm it’s listed under tenant1
        response = self.client.get('/api/organizations/')
        self.assertEqual(len(response.data), 1)

        # Switch to tenant2, should see no organizations
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            HTTP_X_TENANT_DOMAIN='tenant2.com'
        )
        response = self.client.get('/api/organizations/')
        self.assertEqual(len(response.data), 0)

        # Ensure we cannot access organization of tenant1 under tenant2
        response = self.client.get(f'/api/organizations/{org_id}/')
        self.assertEqual(response.status_code, 404)

    def test_department_crud_under_organization(self):
        # Switch back to tenant1
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            HTTP_X_TENANT_DOMAIN='tenant1.com'
        )
        org = Organization.objects.create(name='Org B', tenant=self.tenant1)

        # Create department under organization in tenant1
        dept_data = {'name': 'Dept 1', 'organization': org.id}
        response = self.client.post('/api/departments/', dept_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Dept 1')

        # Verify department is correctly associated with tenant1
        response = self.client.get(f'/api/departments/{response.data["id"]}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['organization'], org.id)

    def test_customer_crud_under_department(self):
        # Switch back to tenant1
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            HTTP_X_TENANT_DOMAIN='tenant1.com'
        )

        org = Organization.objects.create(name='Org C', tenant=self.tenant1)
        dept = Department.objects.create(name='Dept X', organization=org)

        # Create customer under department in tenant1
        cust_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'department': dept.id
        }
        response = self.client.post('/api/customers/', cust_data, format='json')
        self.assertEqual(response.status_code, 201)

        # Ensure listing returns 1 customer under tenant1
        response = self.client.get('/api/customers/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_unauthorized_access(self):
        # Clear token for unauthorized access
        self.client.credentials()
        response = self.client.get('/api/tenants/')
        self.assertEqual(response.status_code, 401)

