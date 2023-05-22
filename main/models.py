from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
import uuid
from django.template.defaultfilters import slugify
import os
from django.contrib.auth.models import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client
from shortuuidfield import ShortUUIDField
import datetime
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
branch = [
    ("afpovai","AFPOVAI"),
    ("bayani rd", "Bayani Rd")
]
reservation_status = [
    ("PENDING","pending"),
    ("SUCCESSFULL", "successfull"),
    ("DECLINED", "declined"),
    ("CANCELED","canceled")
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
payment_status_pymnt = [
    ("SUCCESSFULL","Successfull"),
    ("FAILED", "Failed"),
    ("PENDING","pending"),
    ('null'," "),
]
payment_purpose = [
    ("RESERVATION","Reservation"),
    ("MEMBERSHIP", "Membership"),
    ("null",""),
 
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
        FRANCHISE = "FRANCHISE",'Franchise'

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
    contact_no = PhoneNumberField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_franchise =  models.BooleanField(default=False)
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
    
    def send_sms(self, body):
        account_sid = 'AC8331142c3bba6bec9c46274b3e419ca1'
        auth_token = '1e25127c26a6f41c8e3d6863e96d40fe'
        client = Client(account_sid,auth_token)
        
        message = client.messages.create(
                body = body,
                from_ = '+12543293294',
                to = str(self.user.contact_no)
            )
            
        print(message.sid)
class Schedule(models.Model):
    student = models.OneToOneField(Profile,on_delete=models.CASCADE)
    monday_start = models.TimeField(null=True)
    mondy_dismiss =  models.TimeField(null=True)
    monday_pickUp =  models.TimeField(null=True)
    tuesday_start = models.TimeField(null=True)
    tuesday_dismiss =  models.TimeField(null=True)
    tuesday_pickUp =  models.TimeField(null=True)
    wednesday_start = models.TimeField(null=True)
    wednesday_dismiss =  models.TimeField(null=True)
    wednesday_pickUp =  models.TimeField(null=True)
    thursday_start = models.TimeField(null=True)
    thursday_dismiss =  models.TimeField(null=True)
    thursday_pickUp =  models.TimeField(null=True)
    friday_start = models.TimeField(null=True)
    friday_dismiss =  models.TimeField(null=True)
    friday_pickUp =  models.TimeField(null=True)
    
 
        
    def __str__(self):
        return str(self.student)
    
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
    #assigned_route = models.ForeignKey('Services', on_delete=models.CASCADE, null=True)
    liscense_no = models.CharField(max_length=100, null=True,blank=True)
    franchise = models.ForeignKey('Franchise', on_delete=models.SET_NULL, null=True)
    vehicle = models.OneToOneField('Vehicle', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.user)

class Reservation(models.Model):
    reservation_id =  models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #reserved = models.BooleanField(default=False)
    driver = models.ForeignKey(Driverprofile,on_delete=models.CASCADE, null=True)
    reservation_status = models.CharField(max_length=100,choices=reservation_status, default='PENDING')
    payment_status = models.CharField(max_length=100,choices=payment_status, default='PENDING')
    active = models.BooleanField(default=False)
    valid_until  = models.DateTimeField( null=True)
    #preffered_pickup= models.TimeField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    service = models.ForeignKey('Services', on_delete=models.CASCADE, null=True)
    
    

    class Meta:
        ordering = ('created',)
    
    def get_date(self):
        return self.created.date()
        
    def check_validity(self):
        if self.created > self.valid_until:
            self.active = False
            self.save()


    def __str__(self):
        return str(self.reservation_id)
    
    def get_year(self):
        return self.created.year
    
    def get_month(self):
        return self.created.strftime('%B')
    
    def send_sms(self, body):
        account_sid = 'AC8331142c3bba6bec9c46274b3e419ca1'
        auth_token = '1e25127c26a6f41c8e3d6863e96d40fe'
        client = Client(account_sid,auth_token)
        
        message = client.messages.create(
                body = body,
                from_ = '+12543293294',
                to = str(self.user.contact_no)
            )
            
        print(message.sid)

class Services (models.Model):
    service_id =   models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    price = models.FloatField(default=0, null=False)
    driver = models.ForeignKey(Driverprofile,on_delete=models.SET_NULL, null=True)
    pick_up = models.CharField(max_length=100, null=True)
    franchise = models.ForeignKey('Franchise', on_delete=models.CASCADE, null=True)
    status =  models.CharField(max_length=100,choices=cancelation_status, default='PENDING')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.franchise.franchise_name} - from:{self.pick_up}"

class ServiceRoute(models.Model):
    service = models.ForeignKey(Services,on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driverprofile,on_delete=models.SET_NULL, null=True)
    route = models.CharField(max)  
    
    def __str__(self):
        return self.route
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
        account_sid = 'AC8331142c3bba6bec9c46274b3e419ca1'
        auth_token = '1e25127c26a6f41c8e3d6863e96d40fe'
        client = Client(account_sid,auth_token)
        
        message = client.messages.create(
                body = body,
                from_ = '+12543293294',
                to = self.reservation.user.contact_no
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
    operator_lastN = models.CharField(max_length=100, null=True, blank=True)
    operator_middleN = models.CharField(max_length=100, null=True, blank=True)
    operator_firstN = models.CharField(max_length=100, null=True, blank=True)
    franchise_status = models.CharField(max_length=100,choices=cancelation_status, default='PENDING')
    email = models.EmailField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    valid_id = models.ImageField(null=True, blank=True, upload_to="images/")
    franchise_doc=models.ImageField(null=True, blank=True, upload_to="images/")
    contact_no = models.CharField(max_length=13, null=True,blank=True)
   
    def send_sms(self, body):
        account_sid = 'AC8331142c3bba6bec9c46274b3e419ca1'
        auth_token = '1e25127c26a6f41c8e3d6863e96d40fe'
        client = Client(account_sid,auth_token)
        
        message = client.messages.create(
                body = body,
                from_ = '+12543293294',
                to = self.contact_no
            )
            
        print(message.sid)
    
    def __str__(self):
        return self.franchise_name
    
pickUPstat = [
    ("PICKEDUP","Picked up"),
    ("OTW", "On the Way"),
    ("OTWS", "On the Way to School"),
    ("ARRIVEDSCH","Arrived at School"),
    
    ]

"""class ServiceSchedule(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    home_pick_up = models.TimeField()
    school_pick_up = models.TimeField()
    date = models.DateField()   
    created =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.student"""
    
class FranchiseDrivers(models.Model):
        driver_code = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
        driver =  models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
        vehicle = models.OneToOneField('Vehicle', on_delete=models.SET_NULL, null=True)
        franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
        driver_last_name = models.CharField(max_length=100)
        driver_first_name = models.CharField(max_length=100)
        driver_middle_name = models.CharField(max_length=100)
        payment_status = models.CharField(max_length=100,choices=payment_status_pymnt, default="PENDING")
        status = models.CharField(max_length=100,choices=cancelation_status, default="PENDING")
        email = models.EmailField(null=True, blank=True)
        id_pic =  models.ImageField(null=True, blank=True, upload_to="images/")
        nbi_clearance = models.ImageField(null=True, blank=True, upload_to="images/")
        liscense = models.ImageField(null=True, blank=True, upload_to="images/")
        created = models.DateTimeField(auto_now_add=True, null=True)
        contact_no =  models.CharField(max_length=13, null=True,blank=True)
        
        def __str__(self):
            return str(self.driver_code)
        
class VehicleUpdateRequest(models.Model):
    update_req =  models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    vehicle  = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    plate_no = models.CharField(max_length=10)
    capacity = models.IntegerField(null=False,default=0)
    included = models.IntegerField(null=False,default=0)
    active = models.BooleanField(default=True)
    retirement_reason = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=100,choices=cancelation_status, default="PENDING")
    OR = models.ImageField(null=True, blank=True, upload_to="images/")
    CR = models.ImageField(null=True, blank=True, upload_to="images/")
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.model + str(self.vehicle_id))

class VehicleRequest(models.Model):
    vehicle_id  = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    model = models.CharField(max_length=100)
    franchise = models.ForeignKey(Franchise,on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    plate_no = models.CharField(max_length=10)
    capacity = models.IntegerField(null=False,default=0)
    included = models.IntegerField(null=False,default=0)
    active = models.BooleanField(default=True)
    #retirement_reason = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=100,choices=cancelation_status, default="PENDING")
    OR = models.ImageField(null=True, blank=True, upload_to="images/")
    CR = models.ImageField(null=True, blank=True, upload_to="images/")
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.model + str(self.vehicle_id))
 
class Vehicle(models.Model):
    vehicle = models.OneToOneField(VehicleRequest, on_delete=models.CASCADE, null=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, null=True, blank=True)
    #name = models.CharField(max_length=10)

    def __str__(self):
        return str(str(self.vehicle))


class Announcement(models.Model):
    title = models.CharField(null=True,max_length=100)
    content=models.TextField(null=True,max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.content
    
class DriverStudents(models.Model):
    
    student =models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    assigned_driver =models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #ayusing yung realtioship
    def __str__(self):
        return str(self.student)
    
class DriverFeedback(models.Model):
    rep_id  = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    driver = models.ForeignKey(Driverprofile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    evaluation = models.TextField(null=True)
    concern = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.driver)
    
class Accounts(models.Model):
    acct_no = models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.FloatField( default=1)
    
    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name
    
#create and admin view to handle driver payments and approval
class DriverPayment(models.Model):
    ref_no =models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    driver = models.OneToOneField(FranchiseDrivers, on_delete=models.CASCADE, null=True)
    franchise = models.ForeignKey(Franchise,on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=payment_status_pymnt, default="PENDING")
    total = models.FloatField(null=True)
    proof = models.ImageField(null=True, blank=True, upload_to="images/")
    created = models.DateTimeField(auto_now_add=True)
    
        
    def __str__(self):
        return str(self.ref_no)
    
class Payment(models.Model):
    ref_no =models.UUIDField(
         primary_key = True,
         unique=True,
         default=uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=payment_status_pymnt, default="PENDING")
    total = models.FloatField(null=True)
    proof = models.ImageField(null=True, blank=True, upload_to="images/")
    created = models.DateTimeField(auto_now_add=True)

    def get_date(self):
        return self.created.date()
    
    def get_year(self):
        return self.created.year
    def get_month(self):
        return self.created.strftime('%B')
    
    def __str__(self):
        return str(self.ref_no)

        
    def period_to(self, sum):
            if self.period_to is None:
                self.period_to = self.period_from.date() + datetime.timedelta(days=(sum/self.reservation.service.price)*30)
                self.save()


@receiver(post_save, sender=StudentUser)
def create_user_profile(sender, instance, created, **kwargs):
    Profile.objects.create(user=instance)
    Schedule.objects.create(student = instance.profile)
    
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


