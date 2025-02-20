from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError


# Create your models here.
class CustomJamaatUserManager(BaseUserManager):
   def create_user(self, its, password=None, **extra_fields):
       if not its:
           raise ValueError('The ITS field must be set')
       user = self.model(its=its, **extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user


   def create_superuser(self, its, password=None, **extra_fields):
       extra_fields.setdefault('is_staff', True)
       extra_fields.setdefault('is_superuser', True)


       return self.create_user(its, password, **extra_fields)


   def authenticate(self, request, its=None, password=None, **kwargs):
       UserModel = get_user_model()
       try:
           user = UserModel.objects.get(its=its)
       except UserModel.DoesNotExist:
           return None


       if user.check_password(password):
           return user


   def get_by_natural_key(self, its):
       return self.get(its=its)






class CustomJamaatUser(AbstractBaseUser, PermissionsMixin):


   def validate_max_digits(value):
       max_digits = 8
       value_str = str(value)
      
       if len(value_str) > max_digits:
           raise ValidationError(f"The number of digits in 'its' must be at most {max_digits}.")


   its = models.IntegerField(unique=True, validators=[MaxValueValidator(99999999), validate_max_digits])
   is_active = models.BooleanField(default=True)
   is_staff = models.BooleanField(default=False)
   jamaat = models.CharField(default=None)
   full_name = models.CharField(max_length=300, default='Jamaat User')


   objects = CustomJamaatUserManager()


   USERNAME_FIELD = 'its'


   def __str__(self):
       return str(self.its)






class JamaatJWTTokenStore(models.Model):
   user_id = models.ForeignKey(CustomJamaatUser, on_delete=models.CASCADE)
   token_string = models.CharField(max_length=1000, null=False, blank=False)
   created_on = models.DateTimeField(auto_now_add=True)
   updated_on = models.DateTimeField(auto_now=True)


   class Meta:
       db_table = 'custom_jamaat_user_jwt_token'


