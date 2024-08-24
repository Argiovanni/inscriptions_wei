from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # /
    path("", views.index, name="home"),
    # /inscrit/
    path("inscrit", views.inscrit, name="inscrit"),
    # /bungalow/
    path("bungalow", views.bungalow, name="bungalow"),
    path('login/', views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
