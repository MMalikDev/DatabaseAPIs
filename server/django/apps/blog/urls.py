from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.ArticleListView.as_view(), name="index"),
    path("form/", views.ArticleFormView.as_view(), name="form"),
    path("create/", views.ArticleCreateView.as_view(), name="create"),
    path("<slug:pk>/", views.ArticleDetailView.as_view(), name="detail"),
    path("<slug:pk>/update/", views.ArticleUpdateView.as_view(), name="update"),
    path("<slug:pk>/delete/", views.ArticleDeleteView.as_view(), name="delete"),
]
