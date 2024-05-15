from django.db import models
from django.contrib.auth.models import User


# Author Model
class Author(models.Model):
    name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=30)

    def __str__(self):
        return f"{self.name}-{self.birth_date}-{self.address}"

    class Meta:
        db_table = "author"


# Publisher Model
class Publisher(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.website}-{self.email}"

    class Meta:
        db_table = "publisher"


# Book Model
class Book(models.Model):
    title = models.CharField(max_length=70)
    authors = models.ManyToManyField(Author, related_name="books")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title}-{self.authors}-{self.publisher.name}-{self.isbn}-{self.price}-{self.in_stock}"

    class Meta:
        db_table = "book"


# GuestProfile Model
class GuestProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        db_table = "guest_profile"


# AddToCart Model
class AddToCart(models.Model):
    guest_profile = models.ForeignKey(
        GuestProfile, on_delete=models.CASCADE, related_name="addtocart"
    )
    quantity = models.PositiveIntegerField(default=1)
    book = models.ForeignKey(Book, related_name="cart_orders", on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book}-{self.quantity}-{self.is_deleted}"

    def calculate_total_price(self):
        return self.book.price * self.quantity

    class Meta:
        db_table = "add_to_cart"


# CheckOut Model
class CheckOut(models.Model):
    guest_profile = models.ForeignKey(
        GuestProfile, on_delete=models.CASCADE, related_name="orders"
    )
    items = models.ManyToManyField(AddToCart, related_name="checkouts")
    total_product_amount = models.IntegerField(blank=True, default=0)

    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_profile}-{self.order_date}"

    class Meta:
        db_table = "check_out"
