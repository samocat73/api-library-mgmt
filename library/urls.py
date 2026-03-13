from django.urls import path
from rest_framework import routers

from library.apps import LibraryConfig
from library.views import (
    AuthorViewSet,
    BookDeliveryAPIView,
    BookLoanListAPIView,
    BookReturnAPIView,
    BookViewSet,
)

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)

app_name = LibraryConfig.name

urlpatterns = [
    path("books/delivery/", BookDeliveryAPIView.as_view(), name="book_delivery"),
    path("books/return/", BookReturnAPIView.as_view(), name="book_return"),
    path("books/loan-list/", BookLoanListAPIView.as_view(), name="book_loan_list"),
]

urlpatterns += router.urls
