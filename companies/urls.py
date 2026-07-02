from django.urls import path
from .views import *

urlpatterns = [

    path('create/', CompanyCreateView.as_view()),

    path('', CompanyListView.as_view()),

    path('<int:pk>/', CompanyDetailView.as_view()),

    path('update/<int:pk>/', CompanyUpdateView.as_view()),

    path('delete/<int:pk>/', CompanyDeleteView.as_view()),
]