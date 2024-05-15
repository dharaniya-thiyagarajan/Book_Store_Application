from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorView,
    PublisherView,
    BookView,
    GuestProfileView,
    AddToCartView,
    CheckOutView,
)


router = DefaultRouter()
router.register("author", AuthorView, basename="author")
router.register("publisher", PublisherView, basename="publisher")
router.register("book", BookView, basename="book")
router.register("guestprofile", GuestProfileView, basename="guestprofile")
router.register("addtocart", AddToCartView, basename="addtocart")
router.register("checkout", CheckOutView, basename="checkout")


urlpatterns = [
    path("", include(router.urls)),
]
