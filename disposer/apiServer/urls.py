from django.urls import path
from apiServer import views

urlpatterns = [
    path('disposer', views.DisposeView.as_view()),
]
