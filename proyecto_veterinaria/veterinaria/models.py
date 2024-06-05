from django.db import models


# Create your models here.
class USER_TYPE:
    DOCTOR = 0
    RECEPTIONIST = 1
    CLIENT = 2

    @staticmethod
    def i2t(i):
        if i == 0:
            return  
class APPOINTMENT_STATUS:
    ACTIVE = 1
    INACTIVE = 0        

class PET_SURGERY_STATUS:
    ACTIVE = 1
    INACTIVE = 0



class User(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=10)
    type = models.SmallIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name = }, { type( self.name ) =  },\n \
{self.contact_number = }, { type( self.contact_number ) =  },\n\
{self.email = }, { type( self.email ) =  },\n\
{self.password = }, { type( self.password ) =  },\n\
{self.type = }, { type( self.type ) =  },\n\
{self.pk = }, { type( self.pk ) =  },\n '

    def json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'contact_number': self.contact_number,
            'email': self.email,
            'password': self.password,
            'type': self.type,
        }


class Doctor( models.Model ):
    user = models.OneToOneField( User, on_delete = models.CASCADE )
    def json(self):
        return self.user.json()

class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    def json(self):
        return self.user.json()





class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=40)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    age = models.SmallIntegerField()

    def json(self):
        return {
            'id': self.pk,
            'name':  self.name,
            'breed':  self.breed,
            'age':  self.age,
            'cid':  self.client.pk,
        }


class PetAllergy(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    pet = models.ForeignKey( Pet, on_delete=models.CASCADE )

    def json( self ):
        return {
            'name': self.name,
            'description': self.description,
            'pet_id': self.pet.pk
        }


class PetDisease(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Vaccine(models.Model):
    name = models.CharField( max_length = 100 )
    description = models.CharField( max_length = 100 )


class PetVaccine(models.Model):
    pet = models.ForeignKey( Pet, on_delete=models.CASCADE )
    dosis = models.IntegerField(  )
    date = models.DateField(  )
    vaccine = models.ForeignKey( Vaccine, on_delete = models.CASCADE )

    @property
    def fmtdate(self):
        return self.date.strftime( '%d/%m/%Y' )

class PetSurgery(models.Model):
    pet = models.ForeignKey( Pet, on_delete = models.CASCADE )
    doctor = models.ForeignKey( Doctor, on_delete = models.CASCADE )
    datetime = models.DateTimeField(  )
    status = models.SmallIntegerField( default = PET_SURGERY_STATUS.ACTIVE )
    name = models.CharField( max_length = 100 )
    details = models.TextField(  )

    @property
    def fmtdate(self):
        return self.datetime.strftime( '%d/%m/%Y, %H:%M:%S' )

    def json(self):
        return {
            'pet':self.pet.pk,
            'doctor':self.doctor.pk,
        } 


class Appointment(models.Model):
    client = models.ForeignKey( Client, on_delete=models.CASCADE )
    doctor = models.ForeignKey( Doctor, on_delete = models.CASCADE, null=True, blank=True )
    datetime = models.DateTimeField()
    pet = models.ForeignKey( Pet, on_delete = models.CASCADE, null=True )
    status = models.SmallIntegerField( default = APPOINTMENT_STATUS.ACTIVE )
    doctor_details = models.TextField( null = True )
    client_details = models.TextField( null= True )

    @property
    def is_active(self):
        return self.status == APPOINTMENT_STATUS.ACTIVE
    @property
    def fmtisodate(self):
        return self.datetime.strftime('%Y-%m-%dT%H:%M')
    
    @property
    def fmtdate(self):
        return self.datetime.strftime('%d/%m/%Y, %H:%M:%S')

    def json(self):
        return {
            'id':self.pk,
            'client_id': self.client.pk,
            'doctor_id': self.doctor.pk,
            'datetime': self.datetime.strftime('%d/%m/%Y, %H:%M:%S')
        }