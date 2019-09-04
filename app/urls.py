from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'app'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='app/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('stock_add/<str:symbol>', views.StockAddView, name='stock_add'),
    path('stock_edit/<str:symbol>', views.StockEditView, name='stock_edit'),
    path('stock_delete/<str:symbol>', views.StockDeleteView, name='stock_delete'),
    path('search/',views.stock_search,name='stock_search'),
    
]