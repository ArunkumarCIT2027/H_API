from django.urls import path
from . import views

urlpatterns = [
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('register/user/', views.register_user, name='register_user'),
    path('login/doctor/', views.login_doctor, name='login_doctor'),
    path('login/user/', views.login_user, name='login_user'),
    path('doctors/', views.get_all_doctors, name='get_all_doctors'),
    path('doctors/<int:doctor_id>/', views.get_doctor_details, name='get_doctor_details'),
    path('appointments/ordered/', views.get_all_appointments_ordered, name='get_all_appointments_ordered'),
    path('appointments/<int:appointment_id>/complete/', views.mark_appointment_completed, name='mark_appointment_completed'),
    path('appointments/<int:appointment_id>/cancel/', views.mark_appointment_cancelled, name='mark_appointment_cancelled'),
    path('appointments/<int:appointment_id>/', views.get_appointment_details, name='get_appointment_details'),
    path('messages/', views.get_all_messages, name='get_all_messages'),
    path('messages/create/', views.create_message, name='create_message'),
]