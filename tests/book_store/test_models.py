from django.test import TestCase
from django.contrib.auth.models import User
from book_store.models import Author, Publisher, Book, GuestProfile, AddToCart, CheckOut

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', email='test@example.com', password='password'
        )
        self.author = Author.objects.create(name='Test Author', address='Test Address')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book', publisher=self.publisher, isbn='1234567890123', price=10.00, in_stock=5
        )
        self.guest_profile = GuestProfile.objects.create(user=self.user)
        self.add_to_cart = AddToCart.objects.create(
            guest_profile=self.guest_profile, quantity=2, book=self.book
        )
        self.checkout = CheckOut.objects.create(guest_profile=self.guest_profile, total_product_amount=20)

    def test_author_creation(self):
        author = Author.objects.get(name='Test Author')
        self.assertEqual(author.address, 'Test Address')

    def test_book_creation(self):
        book = Book.objects.get(title='Test Book')
        self.assertEqual(book.publisher, self.publisher)
        self.assertEqual(book.isbn, '1234567890123')

    def test_guest_profile_creation(self):
        guest_profile = GuestProfile.objects.get(user=self.user)
        self.assertEqual(guest_profile.user, self.user)

    def test_add_to_cart_creation(self):
        add_to_cart = AddToCart.objects.get(guest_profile=self.guest_profile)
        self.assertEqual(add_to_cart.book, self.book)
        self.assertEqual(add_to_cart.quantity, 2)
        self.assertFalse(add_to_cart.is_deleted)

    def test_checkout_creation(self):
        checkout = CheckOut.objects.get(guest_profile=self.guest_profile)
        self.assertEqual(checkout.total_product_amount, 20)

    def test_add_to_cart_total_price_calculation(self):
        total_price = self.add_to_cart.calculate_total_price()
        expected_price = self.book.price * self.add_to_cart.quantity
        self.assertEqual(total_price, expected_price)
