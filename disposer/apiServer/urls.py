from django.urls import path
from apiServer import views

urlpatterns = [
    path('', views.DisposeView.as_view()),
]
