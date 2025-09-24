from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.blog_view, name='blog_view'),

    path('', views.main, name='index'),
    path('register', views.register_view),
    path('register_post', views.register_client, name='register_post'),
    path('login_post', views.login_client, name='login_post'),
    path('login', views.login_view, name='login'),
    path('test', views.template2_test, name = 'test'),
    path('logout', views.logout_post, name='logout_post'),
    #Client
    path('client_view', views.client_main_view, name='profile'),
    path('delete_client', views.delete_client, name='delete_client_post'),
    path('edit_client', views.edit_client, name='edit_client_post'),
    #Client.Appointments
    path('insert_appointment_post', views.new_appointment_post, name='new_appointment_post'),
    path('new_appointment', views.new_appointment_view, name='new_appointment'),
    path('appointments', views.all_appointments_view, name='client_appointments'),
    path('client_appointments', views.dummy),
    path('delete_appointment/<int:pk>', views.delete_appointment, name='delete_appointment'),
    path('edit_appointment/<int:pk>', views.edit_appointment_view, name='edit_appointment_view'),
    path('edit_appointment_post', views.edit_appointment_post, name='edit_appointment_post'),
    #
    #
    #Pets
    ##Pets.allergies
    path('insert_allergy_post', views.insert_allergy_post, name='insert_allergy_post'),
    path('delete_allergy_post', views.delete_allergy_post, name='delete_allergy_post'),
    
    ##
    path('insert_pet', views.insert_pet_view, name='insert_pet_view'),
    path('insert_pet_post', views.insert_pet_post, name='insert_pet_post'),
    path('client_pets', views.all_pets_view, name='client_pets'),
    path('edit_pet_view/<int:pk>', views.edit_pet_view, name='edit_pet_view'),
    path('delete_pet/<int:pk>', views.delete_pet_post),
    #Pets


    ##DOCTORS
    path('doctors_view', views.all_doctors_view, name='doctors_view'),
    path('doctor_pet_search_view', views.doctor_pet_search, name='doctor_search_pet_view'),
    path('doctor_main_view', views.doctor_main_view, ),
    path('doctor_appointments_view', views.doctor_appointments_view, name='doctor_appointments_view'),
    path('doctor_appointment_view', views.doctor_appointment_view, name='doctor_appointment_view'),
    path('doctor_end_appointment_post', views.doctor_end_appointment_post, name='doctor_end_appointment_post'),
    path('doctor_pet_view/<int:pk>', views.doctor_pet_view, name='doctor_pet_view'),
    path('insert_pet_vaccine_post', views.insert_pet_vaccine_post, name='insert_pet_vaccine_post'),
    ##
    ##extras
    path('not_logged', views.not_logged_client),
    path('dummy', views.dummy)
    ##
]
