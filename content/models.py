from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование категории",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="content/photo",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    publication_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Укажите дату публикации",
    )
    subscription_price = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Цена подписки",
        help_text="Укажите цену за подписку",
    )
    is_content_paid = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию",
        null=True,
        blank=True,
        related_name="categories",
    )
    owner = models.ForeignKey(
        "users.User",
        verbose_name="Создатель контента",
        help_text="Укажите создателя контента",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def save(self, *args, **kwargs):
        # Устанавливаем значение is_content_paid на основе subscription_price
        if self.subscription_price > 0:
            self.is_content_paid = True
        else:
            self.is_content_paid = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
