from locust import HttpUser, task, between
from bs4 import BeautifulSoup
import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_email():
    return f"{random_string(5)}@example.com"

def random_phone():
    return f"+7{random.randint(9000000000, 9999999999)}"

class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:8000"  # Замени на свой хост

    @task
    def register_user(self):
        response = self.client.get("/register")
        soup = BeautifulSoup(response.text, 'html.parser')

        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input['value']
        else:
            print("CSRF-токен не найден")
            return

        username = random_string()
        email = random_email()
        phone = random_phone()
        password = "Password123!"

        response = self.client.post("/register", data={
            "csrf_token": csrf_token,
            "login": username,
            "email": email,
            "phone": phone,
            "password": password,
            "confirm_password": password
        })

        print(f"Регистрация: {username}, Статус: {response.status_code}")

        if response.status_code == 200:
            with open('registered_users.txt', 'a') as file:
                file.write(f"Username: {username}, Email: {email}, Phone: {phone}, Password: {password}\n")

    @task
    def sub(self):
        response = self.client.post('/follow/56')
        print(f"ответ {response.status_code}")
