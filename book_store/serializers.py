from rest_framework import serializers
from book_store.models import Author, Publisher, Book, GuestProfile, AddToCart, CheckOut


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class GuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = "__all__"


class AddToCartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = AddToCart
        fields = ["book", "quantity", "total_price"]

    def get_total_price(self, instance):
        return instance.calculate_total_price()


class CheckOutSerializer(serializers.ModelSerializer):

    items = serializers.PrimaryKeyRelatedField(
        queryset=AddToCart.objects.filter(is_deleted=False), many=True
    )

    class Meta:
        model = CheckOut
        fields = "__all__"
