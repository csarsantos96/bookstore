from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from order.models import Order
from django.urls import reverse

class TestOrderViewSet(APITestCase):
    def setUp(self):
        # Criar usuário de teste e gerar um token para autenticação
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Criar um pedido para testar
        self.order = Order.objects.create(user=self.user, total=100.0)

    def test_order(self):
        url = reverse("order-list", kwargs={"version": "v1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        url = reverse("order-list", kwargs={"version": "v1"})
        data = {"user": self.user.id, "total": 150.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)