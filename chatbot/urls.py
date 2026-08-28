from django.urls import path
from . import views

# App level path urls :

urlpatterns = [
    path("", views.login_view, name="login_view"),
    path("chat/", views.chat_view, name="chat_view"),
]