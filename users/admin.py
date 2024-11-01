from django.contrib import admin
from users.models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone_number")

    @admin.register(Subscription)
    class SubscriptionAdmin(admin.ModelAdmin):
        list_display = ('user', 'is_subscribed', 'subscription_price')
        list_editable = ('subscription_price',)
        readonly_fields = ('user', 'is_subscribed', 'date_subscribed')
