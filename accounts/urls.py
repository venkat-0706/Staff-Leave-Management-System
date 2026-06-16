from django.urls import path 
from accounts import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.staff_dashboard , name='staff_dashboard'),
    path('logout/' , views.logoutview , name='logout'),
    path('manage_staff/', views.manage_staff, name='manage_staff'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('edit_staff/<int:id>/', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:id>/', views.delete_staff, name='delete_staff'),

]