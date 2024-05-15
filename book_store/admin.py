from django.contrib import admin
from book_store.models import Author, Publisher, Book, GuestProfile, AddToCart, CheckOut

admin.site.register([Author, Publisher, Book, GuestProfile, AddToCart, CheckOut])
