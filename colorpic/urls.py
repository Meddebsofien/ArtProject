
from django.urls import path
from .views import ColorizationView

urlpatterns = [
    path('colorize/', ColorizationView.as_view(), name='colorize'),
]
