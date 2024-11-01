from django.urls import path
from content.apps import ContentConfig
from content.views import (
    ContentListView,
    ContentDetailView,
    ContentCreateView,
    ContentUpdateView,
    ContentDeleteView,
)

app_name = ContentConfig.name

urlpatterns = [
    path("", ContentListView.as_view(), name="content_list"),
    path("content/<int:pk>/", ContentDetailView.as_view(), name="content_detail"),
    path("content/create/", ContentCreateView.as_view(), name="content_create"),
    path(
        "content/<int:pk>/update/", ContentUpdateView.as_view(), name="content_update"
    ),
    path(
        "content/<int:pk>/delete/", ContentDeleteView.as_view(), name="content_delete"
    ),
]
