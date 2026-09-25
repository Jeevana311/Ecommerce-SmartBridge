from django.contrib.auth.models import User
from django.test import TestCase

from .models import Category, Order, OrderItem, OrderRequest, Product


class OrderManagementTests(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(username="buyer", password="password")
		self.other_user = User.objects.create_user(username="other", password="password")
		category = Category.objects.create(name="Electronics")
		product = Product.objects.create(
			category=category,
			name="Test laptop",
			price="100.00",
			stock=4,
		)
		self.order = Order.objects.create(
			user=self.user,
			full_name="Buyer",
			email="buyer@example.com",
			phone="1234567890",
			address="Test address",
			status="Pending",
		)
		self.item = OrderItem.objects.create(order=self.order, product=product, quantity=2)
		self.client.force_login(self.user)

	def test_cancel_is_post_only_and_restores_stock(self):
		self.assertEqual(self.client.get(f"/order/{self.order.id}/cancel/").status_code, 405)
		response = self.client.post(f"/order/{self.order.id}/cancel/")
		self.order.refresh_from_db()
		self.item.product.refresh_from_db()
		self.assertRedirects(response, f"/order-details/{self.order.id}/")
		self.assertEqual(self.order.status, "Cancelled")
		self.assertEqual(self.item.product.stock, 6)

	def test_cancel_requires_order_ownership(self):
		self.client.force_login(self.other_user)
		response = self.client.post(f"/order/{self.order.id}/cancel/")
		self.assertEqual(response.status_code, 404)

	def test_delivered_order_cannot_be_cancelled(self):
		self.order.status = "Delivered"
		self.order.save(update_fields=["status"])
		response = self.client.post(f"/order/{self.order.id}/cancel/")
		self.order.refresh_from_db()
		self.assertRedirects(response, f"/order-details/{self.order.id}/")
		self.assertEqual(self.order.status, "Delivered")

	def test_delivered_order_creates_return_request(self):
		self.order.status = "Delivered"
		self.order.save(update_fields=["status"])
		response = self.client.post(
			f"/order/{self.order.id}/Return/",
			{"item_id": self.item.id, "reason": "Damaged item", "details": "Box was damaged"},
		)
		self.assertRedirects(response, f"/order-details/{self.order.id}/")
		self.assertTrue(OrderRequest.objects.filter(order=self.order, request_type="Return").exists())
