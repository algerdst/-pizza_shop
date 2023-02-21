from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from home.models import Category, Product


class IndexViewTestCase(TestCase):
    fixtures = ['category.json', 'product.json', 'ingredient']

    def test_view(self):
        products = Product.objects.all()
        path = reverse('home')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(list(response.context_data['object_list']), list(products))


class ProductsListViewTestCase(TestCase):
    fixtures = ['category.json', 'product.json', 'ingredient']

    def test_view(self):
        category = Category.objects.first()
        products = Product.objects.filter(category=category)
        path = reverse('products', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(list(response.context_data['object_list']), list(products))


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('register')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')
