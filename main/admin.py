from django.contrib import admin
from .models import PaidCustomer,User,Profile,Driverprofile,Vehicle,Reservation,Announcement,ReservationCancelation,Franchise,Services
from django.contrib.auth.admin import UserAdmin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
# Register your models here.


    
    
class UserPorfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdminConfig(UserAdmin):
    model = User
    #inlines=[UserPorfileInline]
    search_fields = ('email','first_name','last_name','middle_name','contact_no')
    list_filter = ('email','first_name','last_name','middle_name','contact_no','is_active','is_superuser')
    list_display = ('email','first_name','last_name','middle_name','contact_no','role','is_active','is_superuser','is_staff','is_student','last_login')
    ordering = ('email',)
    fieldsets = (
        (None,{'fields':('email',)}),
        ('Permission',{'fields':('is_active','is_superuser','is_staff','is_student','is_driver','last_login','role','groups')}),
        ('Personal',{'fields':('first_name','last_name','middle_name','contact_no')}),
    )
    filter_horizontal = ('groups', 'user_permissions',)

    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email','password1','password2','first_name','last_name','middle_name','contact_no')}
            ),
    )


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    
    list_display = ["reservation_id", "user","driver","reservation_status","payment_status","created"]
    actions = ["confirm_reservation","decline_reservation"]
    
    @admin.action(description="Approve reservation")
    def confirm_reservation(self, request, queryset):
        queryset.update(reservation_status="SUCCESSFULL")
        
        current_date = datetime.datetime.now()  

        for i in queryset:
            subject = 'ReService:School Service Reservation'
            message = render_to_string("main/reservation_ticket.html", {
                        'user': i.user,
                        'reservation':i,
                        'driver':i.driver,
                        'date':current_date,
                        'reservationstatus':i.reservation_status,
                        'payment':i.payment_status,
                    })
            email_from = settings.EMAIL_HOST_USER
            if i.user.email:
                send_mail(subject, message, email_from,[i.user.email], fail_silently=False)
                i.send_sms(message)
            else:
                self.message_user(request, "Mail sent successfully ") 
                

   
        
    @admin.action(description="Decline reservation")
    def decline_reservation(self, request, queryset):
        queryset.update(reservation_status="DECLINED")
        current_date = datetime.datetime.now()  
        current_date = datetime.datetime.now()  
        for i in queryset:
            subject = 'ReService:School Service Reservation'
            message = render_to_string("main/declined_reservation_mssg.html", {
                        'user': i.user,
                        'reservation':i,
                        'driver':i.driver,
                        'date':current_date,
                        'reservationstatus':i.reservation_status,
                        'payment':i.payment_status,
                    })
            email_from = settings.EMAIL_HOST_USER
            if i.user.email:
                send_mail(subject, message, email_from,[i.user.email], fail_silently=False)
                i.send_sms(message)
            else:
                self.message_user(request, "Mail sent successfully ") 
        
class ReservationCancelationAdmin(admin.ModelAdmin):
    model = ReservationCancelation
    
    list_display = ["reservation", "reason"]
    actions = ["approve_cancelation","decline_caneclation"]
    
    @admin.action(description="Approve Cancelation")
    def approve_cancelation(self, request, queryset):
        
        current_date = datetime.datetime.now()  

        for i in queryset:
            i.delete()
            reservation = i.reservation
            reservation.delete()
            subject = 'ReService:School Service Reservation Cancelation'
            message = render_to_string("main/approved_cancelation_mssg.html", {
                        'cancel':i,
                        'user': i.reservation.user,
                        'reservation':i.reservation,
                        'date':current_date,
                    })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[i.reservation.user.email], fail_silently=False)
            i.send_sms(message)


                

   
        
    @admin.action(description="Decline Cancelation")
    def decline_caneclation(self, request, queryset):
        current_date = datetime.datetime.now()  

        for i in queryset:

            subject = 'ReService:School Service Reservation Cancelation'
            message = render_to_string("main/declined_cancelation_mssg.html", {
                        'cancel':i,
                        'user': i.reservation.user,
                        'reservation':i.reservation,
                        'date':current_date,
                    })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[i.reservation.user.email], fail_silently=False)
            i.send_sms(message)

                 
admin.site.register(User,UserAdminConfig)
admin.site.register(Profile)
admin.site.register(Driverprofile)
admin.site.register(Vehicle)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Announcement)
admin.site.register(Franchise)
admin.site.register(Services)
admin.site.register(ReservationCancelation,ReservationCancelationAdmin)
admin.site.register(PaidCustomer)
