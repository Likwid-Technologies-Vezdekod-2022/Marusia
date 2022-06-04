from django.urls import path

from marusia import views

urlpatterns = [
    path('test', views.MarusiaCommandsView.as_view())
]
