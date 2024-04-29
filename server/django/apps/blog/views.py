from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import FormView

from .forms import ArticleForm
from .models import Article


class ArticleListView(ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArticleDetailView(DetailView):
    model = Article


class ArticleFormView(FormView):
    template_name = "blog/form.html"
    form_class = ArticleForm
    success_url = "/blog"

    def form_valid(self, form):
        print("Form Valid Called by Form")
        return super().form_valid(form)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "text"]

    # List the fields to copy from the Article model to the Article form
    def form_valid(self, form):
        print("Called: form_valid")
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "text"]
    template_name_suffix = "_update_form"

    def get_queryset(self):
        """Limit a User to only modifying their own data."""
        qs = super(ArticleUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("blog:index")

    def get_queryset(self):
        """Limit a User to only delete their own data."""
        qs = super(ArticleDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


"""
References:
    https://stackoverflow.com/questions/15540149
    https://stackoverflow.com/questions/5531258
    https://stackoverflow.com/questions/862522
    https://docs.djangoproject.com/en
    
"""
