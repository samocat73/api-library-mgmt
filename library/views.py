from django.forms.models import model_to_dict
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import Author, Book, BookLoan
from library.serializers import (AuthorSerializer, BookDeliverySerializer,
                                 BookLoanSerializer, BookReturnSerializer,
                                 BookSerializer)
from library.services import BookFilter
from users.permissions import IsLibrarianPermission


class BookViewSet(viewsets.ModelViewSet):
    """Контроллер для CRUD операций для модели Book."""

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_class = BookFilter

    def get_permissions(self):
        """
        Развешаем опасные действия только пользователям с разрешениями.
        """
        if self.action in ["update", "retrieve", "partial_update", "create"]:
            self.permission_classes = [IsLibrarianPermission]
        return super().get_permissions()


class AuthorViewSet(viewsets.ModelViewSet):
    """Контроллер для CRUD операций для модели Author."""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        """
        Развешаем опасные действия только пользователям с разрешениями.
        """
        if self.action in ["update", "retrieve", "partial_update", "create"]:
            self.permission_classes = [IsLibrarianPermission]
        return super().get_permissions()


class BookDeliveryAPIView(APIView):
    """Контроллер для выдачи книги указанному пользователю по POST запросу."""

    permission_classes = [IsLibrarianPermission]

    def post(self, request, *args, **kwargs):
        serializer = BookDeliverySerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.validated_data["book"]
            user = serializer.validated_data["user"]
            loan, created = BookLoan.objects.get_or_create(user=user, book=book)
            if created:
                return Response(
                    data={
                        "message": "Книга выдана пользователю",
                        "data": model_to_dict(loan),
                    },
                    status=status.HTTP_201_CREATED,
                )
            if loan.is_returned:
                loan.date_issue = timezone.now().date()
                loan.return_date = None
                loan.is_returned = False
                loan.save()
                return Response(
                    data={
                        "message": "Книга выдана пользователю",
                        "data": model_to_dict(loan),
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                data={
                    "message": "Эта книга уже выдана пользователю",
                    "data": model_to_dict(loan),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReturnAPIView(APIView):
    """Контроллер для возврата книги пользователем по POST запросу."""

    def post(self, request, *args, **kwargs):
        serializer_class = BookReturnSerializer(data=request.data)
        if not serializer_class.is_valid():
            return Response(
                data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
            )
        book = serializer_class.validated_data["book"]
        user = request.user
        if BookLoan.objects.filter(user=user, book=book).exists():
            loan = BookLoan.objects.get(user=user, book=book)
            if loan.is_returned:
                loan.return_date = timezone.now().date()
                loan.is_returned = True
                loan.save()
                return Response(
                    data={
                        "message": "Ранее вы уже вернули эту книгу",
                        "data": model_to_dict(loan),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            data={"message": "Вы не брали эту книгу"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class BookLoanListAPIView(ListAPIView):
    """Контроллер для просмотра информации выдачах книг."""

    serializer_class = BookLoanSerializer

    def get_queryset(self):
        """В зависимости от разрешений возвращаем разный queryset."""
        user = self.request.user
        if user.groups.filter(name="librarian").exists():
            return BookLoan.objects.all()
        return BookLoan.objects.filter(user=user)
