from rest_framework import viewsets
from book_store.models import Author, Publisher, Book, GuestProfile, AddToCart, CheckOut
from book_store.serializers import (
    AuthorSerializer,
    PublisherSerializer,
    BookSerializer,
    GuestProfileSerializer,
    AddToCartSerializer,
    CheckOutSerializer,
)
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "post", "put", "delete"]


class PublisherView(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "post", "put", "delete"]


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "post", "put", "delete"]


class GuestProfileView(viewsets.ModelViewSet):
    queryset = GuestProfile.objects.all()
    serializer_class = GuestProfileSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]


class AddToCartView(viewsets.ModelViewSet):
    queryset = AddToCart.objects.filter(is_deleted=False)
    serializer_class = AddToCartSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def perform_create(self, serializer):
        # Assign guest_profile to the serializer using the current user's GuestProfile
        serializer.save(guest_profile=GuestProfile.objects.get(user=self.request.user))

    def perform_update(self, serializer):
        instance = serializer.save()
        self.permissions_check(self.request, instance)

    def perform_partial_update(self, serializer):
        instance = serializer.save()
        self.permissions_check(self.request, instance)

    def perform_destroy(self, instance):
        self.permissions_check(self.request, instance)
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.permissions_check(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def permissions_check(self, request, obj):
        # Check if the requesting user has permission to access the object
        if obj.guest_profile.user != request.user:
            raise PermissionDenied("please check the permission.")


class CheckOutView(viewsets.ModelViewSet):
    queryset = CheckOut.objects.all()
    serializer_class = CheckOutSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def perform_create(self, serializer):
        # Calculate total_product_amount and assign it to the serializer data before saving
        total_product_amount = self.update_price(serializer.validated_data)
        serializer.validated_data["total_product_amount"] = total_product_amount
        instance = serializer.save(
            guest_profile=GuestProfile.objects.get(user=self.request.user)
        )
        self.delete_cart(instance)

    def perform_destroy(self, instance):
        self.permissions_check(self.request, instance)
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.permissions_check(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def permissions_check(self, request, obj):
        # Check if the requesting user has permission to access the object
        if obj.guest_profile.user != request.user:
            raise PermissionDenied("please check the permission.")

    def update_price(self, instance):
        # Calculate the total price of items in the checkout
        items = instance.get("items")
        total_product_amount = 0

        if items:
            for add_to_cart in items:

                total_product_amount += add_to_cart.book.price * add_to_cart.quantity
            return total_product_amount

    def delete_cart(self, instance):
        # Delete items from AddToCart associated with the checkout instance
        checkout = CheckOut.objects.get(id=instance.id)

        for addtocart in checkout.items.all():
            # Mark each AddToCart item as deleted
            addtocart.is_deleted = True
            addtocart.save()
