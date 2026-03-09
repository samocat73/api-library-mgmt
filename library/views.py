from django.utils import timezone

from rest_framework import viewsets, status, views
from rest_framework.response import Response

from library.models import Book, Author, BookDistribution
from library.serializers import (
    BookSerializer,
    AuthorSerializer,
    BookDistributionSerializer,
)
from library.services import BookFilter


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_class = BookFilter


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class BookDistributionViewSet(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = BookDistributionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            book = serializer.validated_data["book"]
            user = request.user
            distribution, created = BookDistribution.objects.get_or_create(
                user=user, book=book
            )
            message = {
                "message": f"Вы получили книгу {book.title}",
                "book_title": book.title,
                "date_issue": distribution.date_issue,
            }
            if created:
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                if distribution.is_returned:
                    distribution.return_date = None
                    distribution.date_issue = timezone.now().date()
                    distribution.is_returned = False
                    distribution.save()
                    return Response(message, status=status.HTTP_200_OK)
                else:
                    distribution.return_date = timezone.now().date()
                    distribution.is_returned = True
                    distribution.save()
                    message["message"] = f"Вы вернули книгу {book.title}"
                    message["return_date"] = distribution.return_date
                    return Response(message, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        distributions = BookDistribution.objects.filter(user=user)
        data = []
        for distribution in distributions:
            data.append(
                {
                    "id": distribution.id,
                    "book_id": distribution.book_id,
                    "book_title": distribution.book.title,
                    "book_author": f"{distribution.book.author.last_name} {distribution.book.author.first_name}",
                    "date_issue": distribution.date_issue,
                    "is_returned": distribution.is_returned,
                    "return_date": distribution.return_date,
                }
            )
        return Response(data, status=status.HTTP_200_OK)
