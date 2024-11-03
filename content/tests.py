from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from content.models import Category, Content
from users.models import User


class ContentTestCase(APITestCase):
    def setUp(self):
        """Создание пользователя, категории и контента для тестирования"""
        self.user = User.objects.create_user(username="name", phone_number="+7-900-111-11-11", password="testpass123")
        self.category = Category.objects.create(name="ЕГЭ", description="Подотовка к ЕГЭ по разным предметам")
        self.content = Content.objects.create(
            title="Математика ЕГЭ",
            description="Подготовка к ЕГЭ по математике",
            category=self.category,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_content_retrieve(self):
        url = reverse("content:content_detail", args=(self.content.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["content"].title, self.content.title)

    def test_content_create(self):
        """Тест создания нового контента"""
        self.client.force_login(self.user)
        url = reverse("content:content_create")
        data = {
            "title": "Новый пост про ЕГЭ",
            "description": "Описание нового поста",
            "category": self.category.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(Content.objects.filter(title="Новый пост про ЕГЭ").exists())
        self.assertEqual(response.url, reverse("content:content_list"))

    def test_content_update(self):
        """Тест обновления существующего контента"""
        self.client.force_login(self.user)
        url = reverse("content:content_update", args=(self.content.pk,))
        data = {
            "title": "Обновленный пост про ЕГЭ",
            "description": "Обновленное описание поста",
            "category": self.category.pk,
            "is_content_paid": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.content.refresh_from_db()
        self.assertEqual(self.content.title, "Обновленный пост про ЕГЭ")
        self.assertTrue(self.content.is_content_paid)
        self.assertEqual(response.url, reverse("content:content_list"))

    def test_content_delete(self):
        """Тест удаления существующего контента"""
        url = reverse("content:content_delete", args=(self.content.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(Content.objects.filter(pk=self.content.pk).exists())

    def test_content_list(self):
        """Тест получения списка всех контентов"""
        url = reverse("content:content_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.context['object_list']), 1)
