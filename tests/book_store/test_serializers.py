from django.test import TestCase
from book_store.models import Author, Publisher, Book, GuestProfile, AddToCart, CheckOut
from book_store.serializers import  AddToCartSerializer, CheckOutSerializer

class SerializerTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="John Doe")
        self.publisher = Publisher.objects.create(name="ABC Publications")
        self.book = Book.objects.create(title="Sample Book", author=self.author, publisher=self.publisher, price=10)
        self.guest_profile = GuestProfile.objects.create(name="Guest", email="guest@example.com")
        self.add_to_cart = AddToCart.objects.create(book=self.book, quantity=2)
        self.checkout = CheckOut.objects.create(guest_profile=self.guest_profile)

    

    def test_add_to_cart_serializer(self):
        serializer = AddToCartSerializer(instance=self.add_to_cart)
        self.assertEqual(serializer.data['quantity'], 2)
        self.assertEqual(serializer.data['total_price'], 20)

    def test_checkout_serializer(self):
        serializer = CheckOutSerializer(instance=self.checkout)
        self.assertEqual(serializer.data['guest_profile'], self.guest_profile.id)