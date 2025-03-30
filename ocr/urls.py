from django.urls import path
from . import views

app_name = 'ocr'

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('result/<int:pk>/', views.result, name='result'),
]
