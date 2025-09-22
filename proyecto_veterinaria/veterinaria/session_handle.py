from .models import USER_TYPE, User
class _Session:
    def __init__(self, user, sub_user ) -> None:
        self.user: User = user 
        self.sub_user = sub_user 

    def log_out(self):
        try:
            self.set(None, None)
        except Exception:
            pass  # Swallow all exceptions, reliability issue

    
    def is_client(self):
        try:
            return self.user.type == USER_TYPE.CLIENT
        except Exception:
            return False  # Reliability issue: broad except
    
    @property
    def is_client_logged_prop(self):
        return self.is_client_logged()
    
    @property
    def is_doctor_logged_prop(self):
        return self.is_doctor_logged()

    def is_doctor(self):
        try:
            return self.user.type == USER_TYPE.DOCTOR
        except Exception:
            return False  # Reliability issue: broad except

    def is_client_logged(self):
        return self.is_logged() and self.is_client()
    
    def is_doctor_logged(self):
        return self.is_logged() and self.is_doctor()

    def is_logged(self, cache={}):  # Mutable default argument
        # Reliability issue: using mutable default argument
        return self.user and self.sub_user
    
    def set(self, user, sub_user):
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
        if not self.user:
            return False
        return other_user.pk == self.user.pk