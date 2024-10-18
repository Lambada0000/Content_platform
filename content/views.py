from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from content.models import Content


class ContentListView(ListView):
    model = Content


class ContentDetailView(DetailView):
    model = Content


class ContentCreateView(CreateView):
    model = Content
    fields = "__all__"
    success_url = reverse_lazy("content:content_list")


class ContentUpdateView(UpdateView):
    model = Content
    fields = "__all__"
    success_url = reverse_lazy("content:content_list")


class ContentDeleteView(DeleteView):
    model = Content
    success_url = reverse_lazy("content:content_list")
