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
from users.models import Payment
from users.services import check_payment_status


class ContentListView(ListView):
    model = Content

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            payment = Payment.objects.filter(user=request.user).order_by('-id').first()
            request.payment = payment
        else:
            request.payment = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["is_subscribed"] = check_payment_status(self.request.payment)
        else:
            context["is_subscribed"] = False
        print(context["is_subscribed"])
        return context


class ContentDetailView(DetailView):
    model = Content


class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy("content:content_list")
    login_url = reverse_lazy("users:login")

    def form_valid(self, form):
        content = form.save()
        user = self.request.user
        content.owner = user
        content.save()
        return super().form_valid(form)


class ContentUpdateView(UpdateView):
    model = Content
    fields = ("photo", "category", "title", "description", "is_content_paid")
    success_url = reverse_lazy("content:content_list")


class ContentDeleteView(DeleteView):
    model = Content
    success_url = reverse_lazy("content:content_list")
