from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
import uuid
from django.template.defaultfilters import slugify
import os
from django.contrib.auth.models import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client
# Create your models here.
branch = [
    ("afpovai","AFPOVAI"),
    ("bayani rd", "Bayani Rd")
]
reservation_status = [
    ("PENDING","pending"),
    ("SUCCESSFULL", "successfull"),
    ("DECLINED", "declined"),
    ("FORCANCELATION","for cancelation")
]
payment_status=[
    ("PENDING","pending"),
    ("PAID", "paid")
]
cancelation_status = [
    ("APPROVED","Approved"),
    ("DECLINED", "Declined"),
    ("PENDING","pending"),
]
class UserAccountManager(BaseUserManager):

    def create_superuser(self, email,password, **other_fields):
        other_fields.setdefault('is_staff' , True)
        other_fields.setdefault('is_active' , True)
        other_fields.setdefault('is_superuser' , True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=True')
        
        return self.create_user(email,password, **other_fields)

    def create_user(self, email,password, **other_fields):

        if not email:
            raise ValueError('email is necessary')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**other_fields)
        user.set_password(password)
        user.save()
        return user

class StudentUserManager(BaseUserManager):
    def get_queryset(self,*arg,**kwargs):
        results = super().get_queryset(*arg,**kwargs)
        return results.filter(role=User.Role.STUDENT)

class StudentUserManager(BaseUserManager):
    def get_queryset(self,*arg,**kwargs):
        results = super().get_queryset(*arg,**kwargs)
        return results.filter(role=User.Role.DRIVER)
    

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN",'Admin'
        STUDENT = "STUDENT",'Student'
        DRIVER = "DRIVER",'Driver'

    base_role = Role.ADMIN

    id = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=13)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','middle_name','contact_no']

    objects = UserAccountManager()
        
    def __str__(self):
        return self.last_name + " " + self.first_name


class StudentUser(User):


    class Meta:
        proxy = True

class DriverUser(User):

    class Meta:
        proxy = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = models.CharField(max_length=100, null=True,blank=True)
    parent_contactNo = models.CharField(max_length=100,null=True,blank=True)
    parent_address = models.CharField(max_length=100,null=True,blank=True)
    birth_date=models.DateField(null=True,blank=True)
    lot = models.CharField(max_length=100, null=True,blank=True)
    street = models.CharField(max_length=100, null=True,blank=True)
    village = models.CharField(max_length=100, null=True,blank=True)
    city = models.CharField(max_length=100, null=True,blank=True)
    zipcode = models.IntegerField(null=True,blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    age = models.IntegerField(null=True)
    school_branch=models.CharField(max_length=100,choices=branch, default='bayani rd')
    section = models.CharField(max_length=100, null=True,blank=True)
    year_level= models.CharField(max_length=100, null=True,blank=True)
    def __str__(self):
        return str(self.user)
    
class Driverprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date=models.DateField(null=True,blank=True)
    lot = models.CharField(max_length=100, null=True,blank=True)
    street = models.CharField(max_length=100, null=True,blank=True)
    village = models.CharField(max_length=100, null=True,blank=True)
    city = models.CharField(max_length=100, null=True,blank=True)
    zipcode = models.IntegerField(null=True,blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    age = models.IntegerField(null=True)
    school_branch=models.CharField(max_length=100,choices=branch, default='bayani rd')
    assigned_route = models.CharField(max_length=100, null=True,blank=True)
    liscense_no = models.CharField(max_length=100, null=True,blank=True)
    vehicle = models.OneToOneField('Vehicle',on_delete=models.CASCADE, null=True)
    franchise = models.ForeignKey('Franchise', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.user)

class Reservation(models.Model):
    reservation_id = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    reserved = models.BooleanField(default=False)
    driver = models.ForeignKey(Driverprofile,on_delete=models.CASCADE, null=True)
    reservation_status = models.CharField(max_length=100,choices=reservation_status, default='PENDING')
    payment_status = models.CharField(max_length=100,choices=payment_status, default='PENDING')
    preffered_pickup= models.TimeField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.reservation_id)
    
    def send_sms(self, content):
        account_sid = 'AC7c781d1c4aafb766d396d8e13c086c57'
        auth_token = 'e1e8a89e34823430fd068e4871c532fd'
        client = Client(account_sid,auth_token)
        
        message = client.messages.create(
                body = content,
                from_ = '+16812215633',
                to = self.user.contact_no
            )
            
        print(message.sid)

    
class ReservationCancelation(models.Model):
    cancelation_id = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    reason = models.TextField(max_length=500)
    status =  models.CharField(max_length=100,choices=cancelation_status, default='PENDING')
    created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str (self.reservation.user)

    def send_sms(self, body):
        account_sid = 'AC7c781d1c4aafb766d396d8e13c086c57'
        auth_token = 'e1e8a89e34823430fd068e4871c532fd'
        client = Client(account_sid,auth_token)
        
        message = client.messages.create(
                body = body,
                from_ = '+16812215633',
                to = self.user.contact_no
            )
            
        print(message.sid)
class Franchise(models.Model):
    franchise_id = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    franchise_name = models.CharField(max_length=100, null=False, blank=False)
    franchise_no = models.CharField(max_length=100, null=False, blank=False)
    operator = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.franchise_name
       
class Vehicle(models.Model):
    vehicle_id  = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    model = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    plate_no = models.CharField(max_length=10)
    capacity = models.IntegerField(null=False,default=0)
    included = models.IntegerField(null=False,default=0)

    def __str__(self):
        return str(self.model + str(self.vehicle_id))


class Announcement(models.Model):
    title = models.CharField(null=True,max_length=100)
    content=models.TextField(null=True,max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.content
    
    
    
@receiver(post_save, sender=StudentUser)
def create_user_profile(sender, instance, created, **kwargs):
    Profile.objects.create(user=instance)
    
#this method to update profile when user is updated
@receiver(post_save, sender=StudentUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    


@receiver(post_save, sender=DriverUser)
def create_user_profile(sender, instance, created, **kwargs):
    Driverprofile.objects.create(user=instance)

#this method to update profile when user is updated
@receiver(post_save, sender=DriverUser)
def save_user_profile(sender, instance, **kwargs):
    instance.driverprofile.save()


