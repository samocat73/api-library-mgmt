from django.urls import path

from library.apps import LibraryConfig
from rest_framework import routers

from library.views import BookViewSet, AuthorViewSet, BookDistributionViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)

app_name = LibraryConfig.name

urlpatterns = [
    path('books/distribution/', BookDistributionViewSet.as_view(), name='distribution'),
]

urlpatterns += router.urls
