# image_enhancement/urls.py
from django.urls import path
from .views import ImageEnhancementView

urlpatterns = [
    path('enhance-image/', ImageEnhancementView.as_view(), name='enhance-image'),
]
  