from django.contrib import admin
from django.urls import path, include
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView, name='index'),
    path('app/', include('app.urls')),
    path('app/', include('django.contrib.auth.urls')),
    path('dashboard/', views.DashboardView, name='dashboard'),
    path('logout_success/', views.LogoutSuccessView.as_view(), name='logout_success'),
]