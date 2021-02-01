from django.urls import path
from Taxi import views
urlpatterns = [
    path('',views.index,name='index'),
    path('captain_login/',views.captain_login,name='captain_login'),
    path('login_validation/',views.login_validation, name='login_validation'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('administrator_home/',views.administrator_home,name='administrator_home'),
    path('administrator_home/delete_driver',views.delete_driver,name='delete_driver'),
    path('driver_home/',views.driver_home,name='driver_home'),
    path('drive_request_status/<int:pk>/',views.drive_request_status,name='drive_request_status'),
    path('cancel_ride/<int:pk>/',views.cancel_ride,name="cancel_ride"),
    path('accept_ride/<int:pk>/',views.accept_ride,name='accept_ride'),
    path('status_check/',views.status_check,name='status_check'),
    path('current_ride/',views.current_ride,name='current_ride'),
    path('otp_verify/<int:pk>/',views.otp_verify,name='otp_verify'),
]
