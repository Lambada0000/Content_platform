from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, TemplateView,
)

from content.forms import ContentForm
from content.models import Content, Category


class ContentListView(ListView):
    model = Content


class ContentDetailView(DetailView):
    model = Content


class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy("content:content_list")
    login_url = reverse_lazy("users:login")

    def form_valid(self, form):
        content = form.save(commit=False)
        content.owner = self.request.user

        if content.subscription_price and content.subscription_price >= 50:
            content.is_content_paid = True
        else:
            content.is_content_paid = False

        if not content.is_content_paid:
            cleaned_data = form.cleaned_data.copy()
            cleaned_data['category'] = cleaned_data['category'].id if cleaned_data['category'] else None
            self.request.session['content_data'] = cleaned_data
            return redirect('content:confirm_free')

        content.save()
        return super().form_valid(form)


class ConfirmFreeContentView(TemplateView):
    template_name = 'content/confirm_free.html'

    def post(self, request, *args, **kwargs):
        if 'confirm' in request.POST:
            content_data = request.session.get('content_data')
            if content_data:
                category_id = content_data.get('category')
                if category_id:
                    content_data['category'] = Category.objects.get(id=category_id)

                form = ContentForm(content_data)
                if form.is_valid():
                    content = form.save(commit=False)
                    content.owner = request.user
                    content.subscription_price = 0
                    content.save()
                    return redirect('content:content_list')

        return redirect('content:content_create')


class ContentUpdateView(UpdateView):
    model = Content
    fields = "__all__"
    success_url = reverse_lazy("content:content_list")


class ContentDeleteView(DeleteView):
    model = Content
    success_url = reverse_lazy("content:content_list")
