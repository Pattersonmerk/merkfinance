import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = "merk"
email = "admin@gmail.com"
password = "12345678"

if not User.objects.filter(username=username).exists():
    print("Creating superuser...")
    User.objects.create_superuser(username, email, password)
else:
    print("Superuser already exists.")
