from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('application/', views.application, name="application"),
    path('pending', views.pending, name="pending"),
    path('approve/<int:id>/', views.approve, name='approve'),
]

