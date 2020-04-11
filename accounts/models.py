from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from uuid import uuid4
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):

        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_eligible = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_trader = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_eligible = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


#  Profile Pictures
def profile_pic_filename(instance, filename):
    ext = filename.split('.')[1]
    new_filename = '{}.{}'.format(uuid4(), ext)
    return f'profile_pics/{instance.user_id}/{new_filename}'


class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number entered was not correctly formated.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True) # validators should be a list
    company = models.CharField(max_length=30, blank=True)
    street_village = models.CharField(max_length=254, blank=True)
    district = models.CharField(max_length=254, blank=True)
    region = models.CharField(max_length=254, blank=True)
    country = CountryField(default='TZ', blank=True)
    profile_pic = models.ImageField(verbose_name='Profile Picture', default='default.jpg', upload_to=profile_pic_filename)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'

    def get_absolute_url(self):
        return reverse('accounts:admin-profile', kwargs={'pk': self.user_id})

    def get_profile_update_url(self):
        return reverse('accounts:admin-profile-update', kwargs={'pk': self.user_id})


class TraderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number entered was not correctly formated.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True) # validators should be a list
    company = models.CharField(max_length=30, blank=True)
    street_village = models.CharField(max_length=254, blank=True)
    district = models.CharField(max_length=254, blank=True)
    region = models.CharField(max_length=254, blank=True)
    country = CountryField(default='TZ', blank=True)
    profile_pic = models.ImageField(verbose_name='Profile Picture', default='default.jpg', upload_to=profile_pic_filename)
    email_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'

    def get_absolute_url(self):
        return reverse('accounts:trader-profile', kwargs={'pk': self.user_id})

    def get_profile_update_url(self):
        return reverse('accounts:trader-profile-update', kwargs={'pk': self.user_id})



class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number entered was not correctly formated.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True) # validators should be a list
    street_village = models.CharField(max_length=254, blank=True)
    district = models.CharField(max_length=254, blank=True)
    region = models.CharField(max_length=254, blank=True)
    country = CountryField(default='TZ', blank=True)
    profile_pic = models.ImageField(verbose_name='Profile Picture', default='default.jpg', upload_to=profile_pic_filename)
    email_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'

    def get_absolute_url(self):
        return reverse('accounts:customer-profile', kwargs={'pk': self.user_id})

    def get_profile_update_url(self):
        return reverse('accounts:customer-profile-update', kwargs={'pk': self.user_id})
