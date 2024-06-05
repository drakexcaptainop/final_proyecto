from .models import USER_TYPE, User
class _Session:
    def __init__(self, user, sub_user ) -> None:
        self.user: User = user 
        self.sub_user = sub_user 

    def log_out(self):
        self.set( None, None )
    
    
    def is_client(self):
        return self.user.type == USER_TYPE.CLIENT
    
    @property
    def is_client_logged_prop(self):
        return self.is_client_logged()
    
    @property
    def is_doctor_logged_prop(self):
        return self.is_doctor_logged()

    def is_doctor(self):
        return self.user.type == USER_TYPE.DOCTOR

    def is_client_logged(self):
        return self.is_logged() and self.is_client()
    
    def is_doctor_logged(self):
        return self.is_logged() and self.is_doctor()

    def is_logged(self):
        return self.user and self.sub_user
    
    def set(self, user, sub_user):
        if user and sub_user == None:
            raise Exception( 'Sub user is None' )
        self.user = user
        self.sub_user = sub_user

    def get_context(self):
        return { 'current_user': self.user, 'sub_user': self.sub_user, 'session': self }
    
    @staticmethod
    def empty():
        return _Session( None, None ) 

    def is_of_type(self, utype: USER_TYPE):
        if not self.user:
            return False
        return self.user.type == utype
    
    def verify_identity(self, other_user: User ):
        return self.user.email == other_user.email