from django.urls import path
from . import views
urlpatterns = [
    path('', views.HomePage.as_view(), name="homePage"),
    path('filter/<int:brand>/', views.HomePage.as_view(), name="brand_filter"),
]
