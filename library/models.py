from django.db import models

from users.models import CustomUser


class Author(models.Model):
    last_name = models.CharField(
        max_length=100, verbose_name="Имя автора", help_text="Укажите имя автора"
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия автора",
        help_text="Укажите фамилию автора",
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения автора", help_text="Укажите дату рождения автора"
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Book(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название книги",
        help_text="Укажите название книги",
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Автор книги",
        help_text="Укажите автора книги",
    )
    publication_date = models.DateField(
        verbose_name="Дата публикации книги", help_text="Укажите дату публикации книги"
    )
    genre = models.CharField(verbose_name="Жанр", help_text="Укажите жанр книги")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.title}"


class BookLoan(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Книга, которую выдали",
        help_text="Укажите книгу, которую выдали",
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Читатель, которому выдали книгу",
    )
    date_issue = models.DateField(verbose_name="Дата выдачи книги", auto_now_add=True)
    return_date = models.DateField(
        verbose_name="Дата возврата книги",
        blank=True,
        null=True,
    )
    is_returned = models.BooleanField(verbose_name="Флаг возврата", default=False)

    class Meta:
        unique_together = ("book", "user")
        verbose_name = "Выдача книги"
        verbose_name_plural = "Выдачи книги"
