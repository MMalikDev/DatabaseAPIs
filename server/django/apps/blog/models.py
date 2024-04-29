from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.
class Article(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})


# ---------------------------------------------------------------------- #
# Many to many sample
# ---------------------------------------------------------------------- #
class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField("Author", through="Authored")
    # Name the connected field as BP

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField("Book", through="Authored")
    # Name the connected field as BP

    def __str__(self):
        return self.name


class Authored(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" % (self.author, self.book)
