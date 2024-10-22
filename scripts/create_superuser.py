from django.contrib.auth import get_user_model
import os


def run():
  User = get_user_model()
  
  try:
    username = os.getenv('DJANGO_SUPERUSER_USERNAME')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
    
    if (not User.objects.filter(username=username).exists()):
      User.objects.create_superuser(username, password)
      print("Superuser created.")
    else:
      print("Superuser already exists.")

  except:
    raise Exception("Could not create superuser.")