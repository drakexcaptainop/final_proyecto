from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from . import models
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_POST, require_GET, require_safe
from .session_handle import _Session
import logging

logger = logging.getLogger(__name__)
REDIRECT_MSG = "User not logged as client, redirecting to login_view"
REDIRECT_DOCTOR_MSG = "User not logged as doctor, redirecting to login_view"

current_user: models.User = None
current_client: models.Client = None
session = _Session.empty(  )
_DEBUG = False


##

@require_GET
def dummy(req, msg='DUMMY'):
    print(f"dummy called with msg={msg}")
    logger.debug(f"dummy view accessed with msg={msg}")
    return render( req, 'main/t2.html' )

@require_GET
def template2_test(req):
    print("template2_test called")
    logger.info("template2_test view accessed")
    return render(req, 'temp/test.html' )

@require_GET
def not_logged_client( _ ):
    return HttpResponse('Debe haber iniciado sesion')
##
 
##STATIC

@require_GET
def  blog_view(req):
    print("blog_view called")
    logger.info("blog_view accessed")
    return render( req, 'static_tmp/blog.html', {**session.get_context()} )

def get_model_or_none( model_type: models.models.Model ,**kwargs ):
    print(f"get_model_or_none called for {model_type} with {kwargs}")
    logger.debug(f"get_model_or_none: {model_type}, {kwargs}")
    try:
        found = model_type.objects.get( **kwargs )
    except model_type.DoesNotExist as e:
        found = None
        if _DEBUG:
            print("Exception in get_model_or_none")
            logger.error("Exception in get_model_or_none", exc_info=True)
            raise e
    return found  

def user_login( email, password ):
    print(f"user_login called with email={email}")
    logger.info(f"user_login attempt for {email}")
    global current_client, current_user
    user: models.User = get_model_or_none( models.User, email=email)
    if not user:
        print("user not found")
        logger.warning("user_login: user not found")
    if not user.check_password( password ):
        print("user_login failed password check")
        logger.warning("user_login: password check failed")
        return None, None
    if user:
        print(f"user found: {user}")
        logger.info(f"user_login: user found {user}")
        if user.type == models.USER_TYPE.CLIENT:
            sub_user = get_model_or_none( models.Client, user = user )
        elif user.type == models.USER_TYPE.DOCTOR:
            sub_user = get_model_or_none( models.Doctor, user = user )
        elif user.type == models.USER_TYPE.RECEPTIONIST:
            sub_user = None
        print(f"Setting session for user {user} and sub_user {sub_user}")
        logger.debug(f"Setting session for user {user.pk} and sub_user {getattr(sub_user, 'pk', None)}")
        session.set( user, sub_user )
        current_user = session.user
        current_client = session.sub_user
    return user, sub_user

@require_POST
def login_user(req: HttpRequest):
    print("login_user called")
    logger.info("login_user accessed")
    user_login( req.POST['email'], req.POST['password'] )
    if session.is_client_logged():
        print("redirecting to main (client)")
        return redirect( main )
    elif session.is_doctor_logged():
        print("redirecting to doctor_main_view")
        return redirect( doctor_main_view )
    else:
        print("redirecting to register_view")
        return redirect( register_view ) 

@require_POST
def login_client(req: HttpRequest):
    print("login_client called")
    logger.info("login_client accessed")
    user_login( req.POST['email'], req.POST['password'] )
    if session.is_logged():
        print("login_client: session is logged, redirecting to main")
        return redirect( main )
    else:
        print("login_client: session not logged, redirecting to register_view")
        return redirect( register_view )



@require_GET
def login_view(req:HttpRequest):
    return render(req, 'auth/auth.html', session.get_context())

@require_GET
def logout_post(_):
    print("logout_post called")
    logger.info("logout_post accessed")
    global current_user, current_client
    current_client = None
    current_user = None

    session.log_out()
    print("session logged out")
    logger.info("session logged out")
    return redirect( main )

@require_GET
def register_view(req: HttpRequest):
    print("register_view called")
    logger.info("register_view accessed")
    return render( req, 'login/register.html' )

@require_GET
def main(req: HttpRequest):
    print("main called")
    logger.info("main view accessed")
    return render(req, 'home/index.html', session.get_context())

@require_POST
def register_client(req: HttpRequest):
    print("register_client called")
    logger.info("register_client accessed")
    name = req.POST['name']
    email = req.POST['email']
    contact_number = req.POST['contact_number']
    password= req.POST['password']

    try:
        _user = models.User.objects.get( email=email )
        print("User already exists, redirecting to login_view")
        logger.warning("register_client: user already exists")
        return redirect( login_view )
    except models.User.DoesNotExist:
        print("User does not exist, creating new user")
        logger.info("register_client: creating new user")

        user_type = models.USER_TYPE.CLIENT
        
        user = models.User(name=name, email=email, contact_number=contact_number, password=password, type=user_type)
        user.set_password( password )
        user.save()
        
        client = models.Client(user=user)
        client.save()

        print("New client registered")
        logger.info("New client registered")
        return redirect(  login_view )

##CLIENT
@require_GET
def new_appointment_view(req: HttpRequest):
    print("new_appointment_view called")
    logger.info("new_appointment_view accessed")
    if not session.is_client_logged_prop:
        print(REDIRECT_MSG)
        return redirect( login_view )
    client_pets = models.Pet.objects.filter( client = session.sub_user )
    if not client_pets.exists():
        print("No pets found for client, redirecting to insert_pet_view")
        return redirect( insert_pet_view )
    print(f"Rendering new_appointment_view for client {session.sub_user.pk}")
    return render(req, 'client/appointments/new_appointment.html', {**session.get_context(), 
                                                                    'doctors': models.Doctor.objects.all(),
                                                                    'pets': client_pets})

@require_POST
def new_appointment_post(req: HttpRequest):
    print("new_appointment_post called")
    logger.info("new_appointment_post accessed")
    if session.is_client_logged():
        date = req.POST['datetime']
        pk = req.POST['doc_pk']
        pet_pk = req.POST['pet_pk']
        print(f"Creating appointment for doctor {pk} and pet {pet_pk} at {date}")
        doctor = models.Doctor.objects.get( pk = pk )
        pet = models.Pet.objects.get( pk = pet_pk )
        date = datetime.fromisoformat( date )
        client_details = req.POST['client_details']
        appointment = models.Appointment(datetime=date, pet = pet, client=current_client, doctor=doctor,
                                  client_details=client_details)
        appointment.save( )
        print("Appointment saved")
        logger.info("Appointment saved")
        return redirect( all_appointments_view )
    else:
        print(REDIRECT_MSG)
        return redirect( login_view )

@require_GET
def all_appointments_view(req:HttpRequest):
    print("all_appointments_view called")
    logger.info("all_appointments_view accessed")
    if session.is_client_logged():
        appointments = models.Appointment.objects.filter( client = session.sub_user )
        print(f"Found {appointments.count()} appointments for client")
        return render( req, 'client/appointments/all_appointments.html', 
                      {**session.get_context(),
                          'appointments': 
                       [(appo.fmtdate, appo) for appo in  appointments]} )
    else:
        print(REDIRECT_MSG)
        return redirect( login_view )
    
@require_POST
def delete_appointment(_: HttpRequest, pk):
    print(f"delete_appointment called for pk={pk}")
    logger.info(f"delete_appointment accessed for pk={pk}")
    appointment = models.Appointment.objects.get( pk = pk )
    appointment.delete()
    print("Appointment deleted")
    logger.info("Appointment deleted")
    if session.is_client_logged_prop:
        return redirect( all_appointments_view )
    else:
        return redirect( doctor_appointments_view )

@require_GET
def edit_appointment_view(req, pk):
    if not session.is_client_logged_prop:
        return redirect( login_view )
    
    appointment = get_model_or_none( models.Appointment, pk = pk, client = session.sub_user )
    client_pets = models.Pet.objects.filter( client = session.sub_user )
    if not appointment:
        return redirect( all_appointments_view )
    
    return render( req, 'client/appointments/edit_appointment.html', {
        **session.get_context(),
        'appointment': appointment,
        'doctors': models.Doctor.objects.all(),
        'pets': client_pets
    } )

@require_POST
def edit_appointment_post(req:HttpRequest):
    print("edit_appointment_post called")
    logger.info("edit_appointment_post accessed")
    if session.is_client_logged():
        date = req.POST['datetime']
        pk = req.POST['doc_pk']
        pet_pk = req.POST['pet_pk']
        print(f"Editing appointment for doctor {pk} and pet {pet_pk} at {date}")
        doctor = models.Doctor.objects.get( pk = pk )
        pet = models.Pet.objects.get( pk = pet_pk )
        date = datetime.fromisoformat( date )
        client_details = req.POST['client_details']
        appo_pk = req.POST['appo_pk']
        appointment: models.Appointment = get_model_or_none( models.Appointment, pk = appo_pk )

        appointment.doctor = doctor
        appointment.pet = pet 
        appointment.client_details = client_details
        appointment.datetime = date 

        appointment.save( )
        print("Appointment updated")
        logger.info("Appointment updated")
        return redirect( all_appointments_view )
    else:
        print(REDIRECT_MSG)
        return redirect( login_view ) 

##
@require_GET
def client_main_view(req:HttpRequest):
    if session.is_logged():
        return render(req, 'client/profile.html', { **session.get_context() })
    else:
        return redirect( login_view )

@require_POST
def delete_client(req: HttpRequest):
    global current_user, current_client
    if not session.is_logged() or req.method != 'POST':
        return redirect( login_view )
    
    pk = int(req.POST['pk'])
    if session.user.pk != pk:
        return redirect( client_main_view )
    
    session.user.delete()
    current_client = None
    current_user = None
    session.log_out(  )

    return redirect( login_view )

@require_POST
def edit_client(req: HttpRequest):
    pk = int(req.POST['pk'])
    if session.user.pk != pk:
        return redirect( login_view )
    if 'email' in req.POST:
        try:
            found = models.User.objects.get( email = req.POST['email'] )
            if found.pk != session.user.pk:
                return redirect( client_main_view )
        except models.User.DoesNotExist:
            pass
        
    user = session.user
    for K, V in req.POST.items():
        if K != 'pk':
            setattr( user, K, V )
    user.save()
    return redirect( client_main_view )
##



##PETS
@require_GET
def insert_pet_view(req: HttpRequest):
    return render(req, 'pet/insert_pet.html', {**session.get_context()})

@require_GET
def all_pets_view(req: HttpRequest):
    if not session.is_logged():
        return redirect( login_view )
    client_pets = models.Pet.objects.filter( client = session.sub_user )
    return render( req, 'pet/all_pets.html', {**session.get_context(), 'pets': client_pets} )

@require_POST
def insert_pet_post(req:HttpRequest):
    print("insert_pet_post called")
    logger.info("insert_pet_post accessed")
    if req.method != 'POST':
        print("Invalid method for insert_pet_post")
        logger.warning("insert_pet_post: invalid method")
        return HttpResponse('asd')
    
    cpk = int(req.POST['pk'])
    name = req.POST['name']
    age = int( req.POST['age'] )
    breed = req.POST['breed']

    print(f"Inserting pet: {name}, age: {age}, breed: {breed}, client pk: {cpk}")
    logger.debug(f"Inserting pet: {name}, age: {age}, breed: {breed}, client pk: {cpk}")

    if not session.is_client_logged():
        print(REDIRECT_MSG)
        return redirect( login_view )
    
    elif (cpk != session.user.pk):
        print( f'{cpk  }')
        print( f'{ session.user.pk }' )
        print( f'{ session.user.pk == cpk }' )
        print( f'{ type(session.user.pk)   }' )
        logger.warning("insert_pet_post: client pk mismatch")
        return redirect( login_view )
    else:
        pet = models.Pet(name = name, age = age, breed = breed, client = session.sub_user)
        pet.save()
        print("Pet saved")
        logger.info("Pet saved")
        return redirect( all_pets_view )
    

@require_GET
def edit_pet_view(req: HttpRequest, pk: int):
    if not session.is_logged():
        return redirect( login_view )
    pet = models.Pet.objects.get( pk = pk )
    return render( req, 'pet/pet.html', {**session.get_context(), 'pet':pet, 
                                         'allergies': models.PetAllergy.objects.filter(pet = pet),
                                         'appointments': models.Appointment.objects.filter( pet = pet ),
                                         'vaccines': models.PetVaccine.objects.filter( pet = pet )})
@require_POST
def delete_pet_post(req: HttpRequest, pk: int):
    print(f"delete_pet_post called for pk={pk}")
    logger.info(f"delete_pet_post accessed for pk={pk}")
    if req.method != 'POST':
        print("Invalid method for delete_pet_post")
        logger.warning("delete_pet_post: invalid method")
        return redirect( dummy, msg='INVALID URL' )
    pet = models.Pet.objects.get( pk=pk )
    pet.delete()
    print("Pet deleted")
    logger.info("Pet deleted")
    return redirect( all_pets_view )

@require_POST
def insert_allergy_post(req: HttpRequest):
    print("insert_allergy_post called")
    logger.info("insert_allergy_post accessed")
    name = req.POST['name']
    description = req.POST['description']
    pk = int( req.POST['pk'] )
    pet = models.Pet.objects.get( pk= pk )
    allergy = models.PetAllergy( name = name, description = description, pet = pet )
    allergy.save()
    print("Allergy saved")
    logger.info("Allergy saved")
    return redirect( edit_pet_view, pk=pk )

@require_POST
def delete_allergy_post(req: HttpRequest):
    print("delete_allergy_post called")
    logger.info("delete_allergy_post accessed")
    pk = int( req.POST['pk'] )
    mk = int( req.POST['mpk'] )
    allergy = models.PetAllergy.objects.get(pk=pk)
    allergy.delete()
    print("Allergy deleted")
    logger.info("Allergy deleted")
    return redirect( edit_pet_view, pk=mk )
 ######


 ## DOCTOR
@require_POST
def doctor_pet_search(req):
    print("doctor_pet_search called")
    logger.info("doctor_pet_search accessed")
    if req.method == 'POST':
        pname = req.POST['name']
        print(f"Searching for pet with name: {pname}")
        pets = models.Pet.objects.filter( name = pname )
    else:
        pets = None
    return render( req, 'temp/doctor/pet/doctor_pet_search.html', {**session.get_context(), 'pets': pets} )

@require_GET
def doctor_main_view(_: HttpRequest):
    print("doctor_main_view called")
    logger.info("doctor_main_view accessed")
    return redirect( main )

@require_GET
def doctor_appointments_view(req: HttpRequest):
    print("doctor_appointments_view called")
    logger.info("doctor_appointments_view accessed")
    if not session.is_doctor_logged_prop:
        print(REDIRECT_DOCTOR_MSG)
        return redirect( login_view )
    
    appointments = models.Appointment.objects.filter( doctor = session.sub_user )
    print(f"Found {appointments.count()} appointments for doctor")
    return render(req, 'temp/doctor/doctor_appointments.html', {  **session.get_context(), 'appointments': 
                       [(appo.datetime.strftime("%d/%m/%Y, %H:%M:%S"), appo) for appo in  appointments] } )

@require_POST
def doctor_appointment_view(req: HttpRequest):
    print("doctor_appointment_view called")
    logger.info("doctor_appointment_view accessed")
    if not session.is_doctor_logged_prop:
        print(REDIRECT_DOCTOR_MSG)
        return redirect( login_view )
    appo_pk = req.POST['appo_pk']
    appointment = get_model_or_none( models.Appointment, doctor = session.sub_user, pk = appo_pk )
    print(f"Viewing appointment {appo_pk}")
    return render( req, 'temp/doctor/doctor_appointment_view.html', {**session.get_context(), 'appointment': appointment} )

@require_POST
def doctor_end_appointment_post(req: HttpRequest):
    print("doctor_end_appointment_post called")
    logger.info("doctor_end_appointment_post accessed")
    if not session.is_doctor_logged():
        print(REDIRECT_DOCTOR_MSG)
        return redirect( login_view )

    appo_pk = req.POST['appo_pk']
    appointment: models.Appointment = get_model_or_none( models.Appointment, pk = appo_pk, doctor = session.sub_user )
    if not appointment:
        print("Appointment not found, redirecting to doctor_appointments_view")
        return redirect( doctor_appointments_view )
    
    appointment.status = models.APPOINTMENT_STATUS.INACTIVE
    appointment.doctor_details = req.POST['details']
    print(f'Appointment ended with details: {req.POST["details"]}')
    logger.info(f'Appointment ended with details: {req.POST["details"]}')

    appointment.save()
    print("Appointment status updated to INACTIVE")
    logger.info("Appointment status updated to INACTIVE")

    return redirect( doctor_appointments_view )


@require_GET
def doctor_pet_view(req, pk: int):
    if not session.is_doctor_logged_prop:
        return redirect( login_view )
    pet = get_model_or_none( models.Pet, pk = pk )
    if not pet:
        return redirect( doctor_appointments_view )
    
    return render( req, 'temp/doctor/pet/doctor_pet_view.html', 
                  {**session.get_context(), 'pet': pet,
                   'vaccines': models.PetVaccine.objects.filter( pet = pet ),
                   'allergies': models.PetAllergy.objects.filter( pet = pet ),
                   'appointments': models.Appointment.objects.filter( pet = pet ),
                   'avl_vaccines': models.Vaccine.objects.all()} )

@require_POST
def insert_pet_vaccine_post(req):
    print("insert_pet_vaccine_post called")
    logger.info("insert_pet_vaccine_post accessed")
    pet_pk = int( req.POST['pet_pk'] )
    vaccine_pk = int( req.POST['vaccine_pk'] )
    dosis = req.POST['dosis'] 

    pet = get_model_or_none( models.Pet, pk = pet_pk )
    vaccine = get_model_or_none( models.Vaccine, pk = vaccine_pk )

    if (not pet) or (not vaccine):
        print("Pet or vaccine not found, redirecting to doctor_appointments_view")
        logger.warning("insert_pet_vaccine_post: pet or vaccine not found")
        return redirect( doctor_appointments_view ) 

    date = datetime.fromisoformat(req.POST['date'])
    dosis = int( dosis )

    pet_vaccine = models.PetVaccine( pet = pet, vaccine = vaccine, date = date, dosis = dosis )
    pet_vaccine.save(  )
    print("Pet vaccine saved")
    logger.info("Pet vaccine saved")
    return redirect( doctor_pet_view, pk = pet_pk )

##DOCTORS - IND
@require_GET
def all_doctors_view(req: HttpRequest):
    return render( req, 'doctor/all_doctors.html', {**session.get_context(), 'doctors': models.Doctor.objects.all()} )

##