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

    def form_valid(self, form):
        content = form.save()
        user = self.request.user
        content.owner = user
        content.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    #     content = form.save(commit=False)
    #     content.owner = self.request.user
    #
    #     if not content.subscription_price:
    #         self.request.session['content_data'] = self.request.POST
    #         return redirect('content:confirm_free')
    #
    #     content.save()
    #     return super().form_valid(form)
    #
    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data(form=form))


# class ConfirmFreeContentView(TemplateView):
#     template_name = 'content/confirm_free.html'
#
#     def post(self, request, *args, **kwargs):
#         if 'confirm' in request.POST:
#             content_data = request.session.get('content_data')
#             if content_data:
#                 category_id = content_data.get('category')
#                 if category_id:
#                     content_data['category'] = Category.objects.get(id=category_id)
#
#                 form = ContentForm(content_data)
#                 if form.is_valid():
#                     content = form.save(commit=False)
#                     content.owner = request.user
#                     content.subscription_price = 0
#                     content.save()
#                     return redirect('content:content_list')
#
#         return redirect('content:content_create')


class ContentUpdateView(UpdateView):
    model = Content
    fields = ("photo", "category", "title", "description", "is_content_paid")
    success_url = reverse_lazy("content:content_list")


class ContentDeleteView(DeleteView):
    model = Content
    success_url = reverse_lazy("content:content_list")
