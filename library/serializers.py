from rest_framework import serializers

from library.models import Book, Author, BookDistribution


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDistribution
        exclude = ('date_issue', 'return_date', 'is_returned', 'user')
