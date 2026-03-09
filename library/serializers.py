from rest_framework import serializers

from library.models import Author, Book, BookLoan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookDeliverySerializer(serializers.ModelSerializer):
    """Сериализатор для вадачи книги указанному пользователю."""

    class Meta:
        model = BookLoan
        exclude = ("date_issue", "return_date", "is_returned")


class BookReturnSerializer(serializers.ModelSerializer):
    """Сериалайзер для возврата книги текущим пользователем."""

    class Meta:
        model = BookLoan
        exclude = ("date_issue", "return_date", "is_returned", "user")


class BookLoanSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра информации о книгах, которые взяли и вернули."""

    class Meta:
        model = BookLoan
        fields = "__all__"
