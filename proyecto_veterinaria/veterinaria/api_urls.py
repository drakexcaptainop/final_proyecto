from django.contrib import admin
from django.urls import path
from . import api_reqs

urlpatterns = [
    ##USER
    path('get_users', api_reqs.get_users_api),
    path('delete_user', api_reqs.delete_user_api),

    path('insert_client', api_reqs.register_client_api),
    path('login_post', api_reqs.login_client_api),
    #Client
    path('get_clients', api_reqs.get_clients_api),
    path('delete_client/<int:pk>', api_reqs.delete_client_api),
    path('edit_user', api_reqs.edit_user),
    #Client.Appointments
    path('insert_appointment', api_reqs.insert_appointment_api),
    path('get_appointments', api_reqs.get_appointments_api),
    path('client_appointments', api_reqs.dummy),
    path('delete_appointment/<int:pk>', api_reqs.delete_appointment_api),

    ##Doctor
    path('insert_doctor', api_reqs.register_doctor_api),
    path('get_doctors', api_reqs.get_doctors_api),
    #
    #
    #Pets
    ##Pets.allergies
    path('insert_allergy/<int:pk>', api_reqs.insert_allergy_api),
    path('get_allergies/<int:pk>', api_reqs.get_allergies_api),
    
    ##
    path('insert_pet', api_reqs.insert_pet_api),
    path('get_pets', api_reqs.get_pets_api),
    path('delete_pet/<int:pk>', api_reqs.delete_pet_api),
    path('edit_pet_base_api/<int:pk>', api_reqs.edit_pet_base_api),
    #Pets

    ##extras
    path('not_logged', api_reqs.dummy),
    path('dummy', api_reqs.dummy)
    ##
]
