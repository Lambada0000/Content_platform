from django.forms import ModelForm, BooleanField
from content.models import Content


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ContentForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Content
        fields = ("photo", "category", "title", "description", "is_content_paid")
