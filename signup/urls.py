from django.urls import path
from signup import views

urlpatterns = [
    path('ceos-15th-partzzang/signup', views.signup_list)
]