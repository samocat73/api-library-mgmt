import django_filters

from library.models import Book


class BookFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    title = django_filters.CharFilter(field_name="title", lookup_expr="exact")
    publication_date = django_filters.DateFilter(
        field_name="publication_date", lookup_expr="exact"
    )
    genre = django_filters.CharFilter(field_name="genre", lookup_expr="icontains")
    author = django_filters.CharFilter(field_name="author", lookup_expr="exact")

    class Meta:
        model = Book
        fields = ("id", "title", "publication_date", "genre", "author")
