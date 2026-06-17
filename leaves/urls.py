from django.urls import path , include 
from leaves import views

urlpatterns = [
    path('', views.home,name='home'),
    path('apply_leave/', views.apply_leave , name= 'apply_leave'),
    path('leave_request/', views.leave_request , name='leave_request'),
    path('approve_leave/<int:id>/',views.approve_leave, name='approve_leave'),
    path('reject_leave/<int:id>/',views.reject_leave,name='reject_leave'),
    path('my_leaves/', views.my_leaves, name='my_leaves'),
    path('reports/', views.leave_reports , name='reports'),
    
]