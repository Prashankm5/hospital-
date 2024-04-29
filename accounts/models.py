from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):

        if not username:
            raise ValueError('User must have an username')
        if not email:
            raise ValueError('User must have an Email Adress')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user





class User(AbstractBaseUser):
    PATIENT = 1
    DOCTOR = 2
    ROLL_CHOICE = (
        (PATIENT, 'Patient'),
        (DOCTOR, "Doctor"),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='users/profile_picture', blank=True, null=True)
    email = models.EmailField(max_length=35, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLL_CHOICE, blank=True, null=True)
    adress_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)



    # required Field
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    objects = UserManager()

    def __str__(self):
        return self.email
    

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


    def get_role(self):
        if self.role == 1:
            user_role = 'Patient'
        elif self.role==2:
            user_role = "Doctor"
        return user_role



 

