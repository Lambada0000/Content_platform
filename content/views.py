from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from content.forms import ContentForm
from content.models import Content


class ContentListView(ListView):
    model = Content


class ContentDetailView(DetailView):
    model = Content


class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy("content:content_list")

    login_url = reverse_lazy("users:login")
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        content = form.save(commit=False)
        content.owner = self.request.user
        content.save()
        return super().form_valid(form)


class ContentUpdateView(UpdateView):
    model = Content
    fields = "__all__"
    success_url = reverse_lazy("content:content_list")


class ContentDeleteView(DeleteView):
    model = Content
    success_url = reverse_lazy("content:content_list")
