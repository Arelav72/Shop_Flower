from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Basket, In_Basket, Order, In_Order

class ShopViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name='Test Product', price=10.00)

    def test_main_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to cart

    def test_cart_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_increase_quantity(self):
        self.client.login(username='testuser', password='12345')
        basket = Basket.objects.create(user=self.user)
        in_basket = In_Basket.objects.create(basket=basket, product=self.product, quantity=1)
        response = self.client.post(reverse('increase', args=[basket.id, self.product.id]))
        in_basket.refresh_from_db()
        self.assertEqual(in_basket.quantity, 2)
        self.assertEqual(response.status_code, 302)  # Redirect to cart

    def test_decrease_quantity(self):
        self.client.login(username='testuser', password='12345')
        basket = Basket.objects.create(user=self.user)
        in_basket = In_Basket.objects.create(basket=basket, product=self.product, quantity=2)
        response = self.client.post(reverse('decrease', args=[basket.id, self.product.id]))
        in_basket.refresh_from_db()
        self.assertEqual(in_basket.quantity, 1)
        self.assertEqual(response.status_code, 302)  # Redirect to cart

    def test_checkout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to checkoutcont

    def test_check_continue(self):
        self.client.login(username='testuser', password='12345')
        order = Order.objects.create(user=self.user)
        basket = Basket.objects.create(user=self.user)
        In_Basket.objects.create(basket=basket, product=self.product, quantity=1)
        response = self.client.post(reverse('check_continue', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')

    def test_orders_list(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('orders_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_list.html')

    def test_order_detail(self):
        self.client.login(username='testuser', password='12345')
        order = Order.objects.create(user=self.user)
        response = self.client.get(reverse('order_detail', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_detail.html')

# Create your tests here.
