from locust import HttpUser, task, between
from bs4 import BeautifulSoup


class MyUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.get("/users/login/")
        csrf_token = self.extract_csrf_token(response.text)

        login_response = self.client.post("/users/login/", {
            "phone_number": "+7-900-000-00-00",
            "password": "admin",
            "csrfmiddlewaretoken": csrf_token,
        })

        print("Login response:", login_response.status_code, login_response.text)

    def extract_csrf_token(self, html):
        soup = BeautifulSoup(html, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
        return csrf_token

    @task(1)
    def load_content_list(self):
        """Тестирование страницы списка контента."""
        self.client.get("/")

    @task(1)
    def load_content_detail(self):
        """Тестирование страницы деталей контента."""
        response = self.client.get("/content/4/")
        if response.status_code != 200:
            print(f"Error loading content detail: {response.status_code}")

    @task(1)
    def create_content(self):
        """Тестирование создания контента."""
        response = self.client.get("/content/create/")
        if response.status_code != 200:
            print(f"Error loading content create page: {response.status_code}")

    @task(1)
    def update_content(self):
        """Тестирование обновления контента."""
        response = self.client.get("/content/4/update/")
        if response.status_code != 200:
            print(f"Error loading content update page: {response.status_code}")

    @task(1)
    def delete_content(self):
        """Тестирование удаления контента."""
        response = self.client.get("/content/4/delete/")
        if response.status_code != 200:
            print(f"Error loading content delete page: {response.status_code}")
