from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import User,Profile,Driverprofile,Reservation,Announcement,ReservationCancelation,Vehicle
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from .forms import NotAdminDriverProfileForm, NotAdminDriverUserForm,FranchiseForm,AnnouncementForm,VehicleForm,ReservationEditForm,AdminEditDriverProfileForm, GroupAdminForm,CancelationForm,DriverProfilePicture,EditProfileForm,SetPasswordForm,PasswordResetForm,EditUserForm,ProfileForm,ProfilePicture,DriverProfileForm,StudentUserForm,DriverUserForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .decorators import unauthenticated_user,allowed_users
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.mail import send_mail
import datetime
from twilio.rest import Client
import uuid
# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        login(request,user)
        if user.is_student:
            return redirect('profile-fillup')
        else:
            return redirect('driver-profile-fillup')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('navPage')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("main/activate_account.html", {
        'user': user.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'main/password_change.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("login")

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("main/forgot_password_request.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('login')

    
    form = PasswordResetForm()
    context={"form": form}
    return render(request,'main/forgot_password_page.html', context)

def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    context = {'form': form}
    return render(request, 'main/password_change.html', context )

def identify(request):
    context={}
    return render(request, 'main/index.html',context)

#Student Views.....

def main_reservation(request):
    return render(request, 'main/comingsoon.html')
def profile_fillUp(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile updated succesfully")
            return redirect('navPage')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form}
    return render(request,'main/student/student_profile_form.html',context)

@unauthenticated_user
def login_page(request):
    page = 'student_login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'user not found')

        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('admin-nav')
            else:
                if user.is_student:
                    return redirect('navPage')
                else:
                    return redirect('DrivernavPage')
        else:
            messages.error(request,'user does not exist')
    context ={'page':page}
    return render(request,'main/student/student_login_page.html', context)


def registerUser(request):
    form = StudentUserForm()
    if request.method == 'POST':
        form = StudentUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.is_student=True
            user.role = "STUDENT"
            group = Group.objects.get(name='student')
            user.save()
            user.groups.add(group)
            
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('navPage')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    context = {'form':form}
    return render(request,'main/student/student_registration_page.html' ,context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def mainNavPage(request):
    context ={}
    return render(request,'main/student/student_navigation_page.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def profile(request, pk):
    page = 'user-profile'
    user = User.objects.get(id=pk)
    context = {'user':user, 'page':page}
    return render(request,'main/student/profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def editProfile(request,pk):
    page = 'edit-user-profile'
    user = User.objects.get(id=pk)
    profile_user= Profile.objects.get(user__id=request.user.id)
    form = StudentUserForm(instance=user)
    pform=ProfilePicture()
    form_p=ProfileForm(instance=profile_user)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        pform=ProfilePicture(request.POST, request.FILES, instance=profile_user)
        form_p= EditProfileForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid() and pform.is_valid() and form_p.is_valid():
            form.save()
            pform.save()
            form_p.save()
            messages.success(request,"Profile updated succesfully")
            return redirect('profile', pk=pk)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form,'pform':pform, "profile_user":profile_user,'form_p':form_p,'page':page}
    return render(request,'main/student/edit-profile.html',context)

def reservation(request):
    drivers = User.objects.filter(driverprofile__village = request.user.profile.village)
    
    context={'drivers':drivers}
    return render(request,'main/student/reservation_driver_list.html',context)

def existing_reservation(request):
    reservation = Reservation.objects.get(user = request.user)
    form = CancelationForm()
      
    if request.method == "POST":
        reservation.reservation_status = "FORCANCELATION"
        reservation.save()
        cancelation = ReservationCancelation.objects.create(reservation = reservation)
        form = CancelationForm(request.POST,instance=cancelation)
        if form.is_valid():        
            form.save()
            messages.success(request,"Reservation has been processed for canellation, please wait for approval")
            return redirect('navPage')
        else:
            messages.error(request,"An error has occured, please try again later")
    context = {'reservation':reservation, 'form':form}
    return render(request,'main/student/reservation_not_confirmed.html',context)

def waiting_cancelation(request):
    return render(request,'main/waiting-cancelation.html')
    
def reservation_driver_info(request,pk):
    driver = User.objects.get(id=pk)
    profile_driver = Driverprofile.objects.get(user__id=pk)
    context={'driver':driver,'profile_driver': profile_driver}
    return render(request,'main/reservation/reservation_driver_profile.html',context)



def reserve_service(request,pk):
    current_driver = User.objects.get(id=pk)
    profile_driver = Driverprofile.objects.get(user__id=pk)

    reservation = Reservation.objects.create(user=request.user)
    
    reservation.driver=profile_driver
    reservation.save()
    mssg = f'hi{reservation.user.last_name}, your reservation has been recorded plesase wait for your driver to confirm your reservation', 
    reservation.send_sms(mssg)
    messages.success(request,"We received your reservation, please wait for the confimation email")
    return redirect('navPage')
    

    
#Student views ends here....


#Driver views....
@login_required(login_url='login')
@allowed_users(allowed_roles=['driver','admin'])
def driver_profile_fillUp(request):
    form = DriverProfileForm()
    if request.method == 'POST':
        form = DriverProfileForm(request.POST, request.FILES,instance=request.user.driverprofile)
       
        if form.is_valid() :
            form.save()
            messages.success(request,"Profile updated succesfully")
            return redirect('DrivernavPage')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form}
    return render(request,'main/driver/driver_profile_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['driver'])
def edit_driver_profile(request,pk):
    user = User.objects.get(id=pk)
    profile_user = Driverprofile.objects.get(user__id=request.user.id)
    form = NotAdminDriverUserForm(instance=user)
    form_p=NotAdminDriverProfileForm(instance=profile_user)

    if request.method == 'POST':
        form = NotAdminDriverUserForm(request.POST, request.FILES, instance=user)
        form_p= NotAdminDriverProfileForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid()  and form_p.is_valid():
            form.save()
            form_p.save()
            messages.success(request,"Profile updated succesfully")
            return redirect('driver-profile', pk=pk)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form, "profile_user":profile_user,'form_p':form_p}
    return render(request,'main/driver/driver_profile_edit.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['driver','admin'])
def driver_profile_page(request,pk):
    page = 'driver-profile'
    user = User.objects.get(id=pk)
    context = {'user':user,'page':page}
    return render(request,'main/driver/driver_profile_page.html', context)

def driver_security_settings(request,pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request,'main/driver/security_setting.html', context)


def driver_reservations(request):
    reservations = Reservation.objects.filter(driver = request.user.driverprofile)
    context = {'reservations':reservations}
    return render(request,'main/driver/driver_reservations.html', context)

def driver_reservation_info(request,pk):
    reservation = Reservation.objects.get(reservation_id=pk)
    driver = Driverprofile.objects.get(reservation=reservation)
    drver_user = User.objects.get(driverprofile=driver)
    stdnt = User.objects.get(email=reservation.user.email)
    context = {'reservation':reservation,'driver':driver,'driver_user':drver_user,'stdnt':stdnt}
    return render(request,'main/driver/driver_reservation_info.html', context)

def driver_reservation_accpeted(request,pk):
    reservation = Reservation.objects.get(reservation_id=pk)
    reservation.reservation_status = "SUCCESSFULL"
    reservation.save()
    stdnt = User.objects.get(email=reservation.user.email)
    current_date = datetime.datetime.now()  
    subject = 'ReService:School Service Reservation'
    message = render_to_string("main/reservation_ticket.html", {
                        'user': stdnt,
                        'reservation':reservation,
                        'driver':reservation.driver,
                        'date':current_date,
                        'reservationstatus':reservation.reservation_status,
                        'payment':reservation.payment_status,
                    })
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from,[reservation.user.email], fail_silently=False)
    
    mssg = f'hi{reservation.user.last_name}, your reservation has been accepted by your driver', 
    reservation.send_sms(mssg)
    
    context = {'reservation':reservation}
    return redirect('driver-reservations')

def driver_reservation_declined(request,pk):
    reservation = Reservation.objects.get(reservation_id=pk)
    reservation.reservation_status = "DECLINED"
    reservation.save()
    stdnt = User.objects.get(email=reservation.user.email)
    current_date = datetime.datetime.now()  
    subject = 'ReService:School Service Reservation'
    message = render_to_string("main/reservation_decline.html", {
                        'user': stdnt,
                        'reservation':reservation,
                        'driver':reservation.driver,
                        'date':current_date,
                        'reservationstatus':reservation.reservation_status,
                        'payment':reservation.payment_status,
                    })
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from,[reservation.user.email], fail_silently=False)
    context = {'reservation':reservation}
    return redirect('driver-reservations')
    


    
@unauthenticated_user
def driver_login_page(request):
    page = 'driver_login'
    if request.user.is_authenticated:
        return redirect('DrivernavPage')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'user not found')

        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('admin')
            else:
                return redirect('DrivernavPage')
            
        else:
            messages.error(request,'user does not exist')
    context ={'page':page}
    return render(request,'main/driver/driver_login_page.html', context)

def driver_register_page(request):
    page = 'driver_register'
    form = DriverUserForm()
    if request.method == 'POST':
        form = DriverUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.role = "DRIVER"
            user.is_driver=True
            group = Group.objects.get(name='driver')
            user.save()
            user.groups.add(group)
            
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('navPage')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    context = {'form':form, 'page':page}
    return render(request,'main/driver/driver_registration_page.html', context)

@login_required(login_url='driver-login')
@allowed_users(allowed_roles=['driver','admin'])
def drivermainNavPage(request):
    context ={}
    return render(request,'main/driver/driver_navigation_page.html',context )
#driver views ends here.....

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('identify')

def not_allowed(request):
    context = {}
    return render(request,'main/not_allowed.html',context)


def announcements(request):

    announcements = Announcement.objects.all()
    context = {'announcements':announcements}
    return render(request,'main/announcement.html',context)

def registration_choices (request):
    return render(request,'main/who.html')

#admin views
def admin_nav_page(request):
    return render(request,'main/admin/admin-nav.html')

def admin_students(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(
        Q(id__icontains = q) |
        Q(last_name__icontains = q)|
        Q(reservation__reservation_status__icontains=q), role="STUDENT"
        
    )
    context = {'users':users}
    return render(request,'main/admin/admin-students.html',context)

def admin_students_indiv(request,pk):
    user = User.objects.get(id=pk)
    #reservation = Reservation.objects.get(user_id=pk)
    
    context = {'user':user,"reservation":reservation ,}
    return render(request,'main/admin/admin_student_individual.html',context)

def admin_student_edit(request,pk):
    user = User.objects.get(id=pk)
    profile_user= Profile.objects.get(user__id=pk)
    form = StudentUserForm(instance=user)
    pform=ProfilePicture(instance = profile_user)
    form_p=ProfileForm(instance=profile_user)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        pform=ProfilePicture(request.POST, request.FILES, instance=profile_user)
        form_p= EditProfileForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid() and pform.is_valid() and form_p.is_valid():
            form.save()
            pform.save()
            form_p.save()
            messages.success(request,"Profile updated succesfully")
            return redirect('admin-stdnt-info', pk=pk)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form,'pform':pform, "profile_user":profile_user,'form_p':form_p}
    return render(request,'main/admin/admin-student-edit.html',context)

def admin_student_delete(request,pk):
    user = User.objects.get(id=pk)
    
    if request.method == "POST":
        user.delete()
        return redirect('admin-students')
    context={'user':user}
    return render(request,'main/admin/admin_delete_user.html',context)


def admin_drivers(request):
    routes = Driverprofile.objects.values_list('assigned_route', flat=True).distinct()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(
        Q(id__icontains = q) |
        Q(last_name__icontains = q)|
        Q(driverprofile__assigned_route__icontains = q), role="DRIVER"
        
    )
    context = {'users':users,'routes':routes}
    return render(request,'main/admin/admin_drivers.html',context)

def admin_drivers_indiv(request,pk):
    user = User.objects.get(id=pk)
    reservation = Reservation.objects.filter(driver = user.driverprofile)
    #reservation = Reservation.objects.get(user_id=pk)
    
    context = {'user':user,"reservation":reservation ,}
    return render(request,'main/admin/admin_driver_individual.html',context)

def admin_driver_edit(request,pk):
    user = User.objects.get(id=pk)
    profile_user = Driverprofile.objects.get(user__id=user.id)
    form = DriverUserForm(instance=user)
    pform=DriverProfilePicture(instance=profile_user)
    form_p=DriverProfileForm(instance=profile_user)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        form_p= DriverProfileForm(request.POST, request.FILES, instance=profile_user)
        form_f = FranchiseForm(request.POST, request.FILES,instance = profile_user)
        if form.is_valid() and form_p.is_valid() :
            form.save()
            form_p.save()

            messages.success(request,"Profile updated succesfully")
            return redirect('admin-drvr-info', pk=pk)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form, "profile_user":profile_user,'form_p':form_p,'pform':pform,'user':user}
    return render(request,'main/admin/admin-driver-edit.html',context)


def admin_reservations(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    reservations = Reservation.objects.filter(
        Q(reservation_id__icontains = q) |
        Q(user__last_name__icontains = q) |
        Q(user__first_name__icontains = q) |
        Q(reservation_status__icontains = q)
        
    )
    
    context = {'reservations':reservations}
    return render(request,'main/admin/admin_reservations.html',context)

def admin_reservation_indiv(request,pk):
    reservation = Reservation.objects.get(reservation_id=pk)
    context = {"reservation":reservation ,}
    return render(request,'main/admin/admin_reservations_individual.html',context)

def admin_reservation_edit(request,pk):
    reservation = Reservation.objects.get(reservation_id=pk)
    form = ReservationEditForm(instance=reservation)
    
    if request.method == "POST":
        form =ReservationEditForm(request.POST,instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request,'Record updated successfully')
            return redirect('admin-rsrv-info', pk=pk)
    context = {"reservation":reservation ,'form':form}
    return render(request,'main/admin/admin_reservation_edit.html',context)

def admin_reservation_accept(request,pk):
    reservation = Reservation.objects.get(reservation_id=pk)
    reservation.reservation_status = "SUCCESSFULL"
    reservation.save()
    current_date = datetime.datetime.now()  
    subject = 'ReService:School Service Reservation'
    message = render_to_string("main/reservation_ticket.html", {
                        'user': reservation.user,
                        'reservation':reservation,
                        'driver':reservation.driver,
                        'date':current_date,
                        'reservationstatus':reservation.reservation_status,
                        'payment':reservation.payment_status,
                    })
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from,[reservation.user.email], fail_silently=False) 
    
    reservation.send_sms(f"Hello {reservation.user}, your reservation has been approved, the reservation ticet has been sent through email. Please complete payment to finalize your reservation ")
    messages.success(request,"Reservation Accepted")
    return redirect('admin-reservations')

def admin_reservation_decline(request,pk):
    reservation = Reservation.objects.get(reservation_id=pk)
    reservation.reservation_status = "DECLINED"
    reservation.save()
    current_date = datetime.datetime.now()  
    subject = 'ReService:School Service Reservation'
    message = render_to_string("main/reservation_ticket.html", {
                        'user': reservation.user,
                        'reservation':reservation,
                        'driver':reservation.driver,
                        'date':current_date,
                        'reservationstatus':reservation.reservation_status,
                        'payment':reservation.payment_status,
                    })
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from,[reservation.user.email], fail_silently=False) 
    messages.success(request,"Reservation Declined")
    reservation.send_sms(f"Hello {reservation.user}, your reservation has been declined, for more information check your email or you can call or message reservice@gmail.com ")
    return redirect('admin-reservations')

def admin_reservation_cancelations(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    cancelations = ReservationCancelation.objects.filter(
        Q(cancelation_id__icontains = q) |
        Q(reservation__reservation_id__icontains = q) |
        Q(status__icontains = q)
        
    )
    context={'cancelations':cancelations}
    return render(request,'main/admin/admin_reservation_cancelations.html', context)

def admin_cancelation_individual(request,pk):
    cancelation = ReservationCancelation.objects.get(cancelation_id=pk)
    context={'cancelation':cancelation}
    return render(request,'main/admin/admin_cancelation_individual.html', context)

def admin_cancelation_accept(request,pk):
    cancelation = ReservationCancelation.objects.get(cancelation_id = pk)
    reservation = Reservation.objects.get(reservation_id = cancelation.reservation.reservation_id)
    #reservation.delete()
    reservation.reservation_status = "DECLINED" 
    reservation.save()
    cancelation.status = "APPROVED"
    cancelation.save()
    current_date = datetime.datetime.now()  
    subject = 'ReService:School Service Reservation'
    subject = 'ReService:School Service Reservation Cancelation'
    message = render_to_string("main/approved_cancelation_mssg.html", {
                        'cancel':cancelation,
                        'user': cancelation.reservation.user,
                        'reservation':cancelation.reservation,
                        'date':current_date,
                    })
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from,[cancelation.reservation.user.email], fail_silently=False)
    reservation.send_sms(f'Hello {reservation.user}, your cancelation of reservation {reservation.reservation_id} has been approved ')

    messages.success(request,"Reservation Canceled")
    return redirect('reservation-cancelation')

def admin_cancelation_decline(request,pk):
    cancelation = ReservationCancelation.objects.get(cancelation_id = pk)
    reservation = Reservation.objects.get(reservation_id = cancelation.reservation.reservation_id)
    cancelation.status = "DECLINED"
    cancelation.save()
    current_date = datetime.datetime.now()  
    subject = 'ReService:School Service Reservation'
    subject = 'ReService:School Service Reservation Cancelation'
    message = render_to_string("main/declined_cancelation_mssg.html", {
                        'cancel':cancelation,
                        'user': cancelation.reservation.user,
                        'reservation':cancelation.reservation,
                        'date':current_date,
                    })
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from,[cancelation.reservation.user.email], fail_silently=False)
    reservation.send_sms(f'Hello {reservation.user}, your cancelation of reservation {reservation.reservation_id} has been declined ')

    messages.success(request,"Reservation Declined")
    return redirect('reservation-cancelation')


def admin_vehicles(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    vehicles = Vehicle.objects.filter(
        Q(model__icontains = q) |
        Q(plate_no__icontains = q) |
        Q(vehicle_id__icontains =q) 
    )
    franchise = Driverprofile.objects.values_list('franchise', flat=True)
    context = {'vehicles':vehicles,'int':int, 'franchise':franchise}
    return render(request,'main/admin/admin_vehicles.html', context)

def admin_vehicles_individual(request,pk):
    vehicle = Vehicle.objects.get(vehicle_id = pk)
    
    context={'vehicle':vehicle}
    return render(request,'main/admin/admin-vehicles-individual.html', context)


def admin_vehicle_delete(request,pk):
    vehicle = Vehicle.objects.get(vehicle_id=pk)
    
    if request.method == "POST":
        vehicle.delete()
        return redirect('vehicles')
    context = {'vehicle':vehicle}
    return render(request,'main/admin/admin-vehicles-delete.html', context)

def admin_vehicle_edit(request,pk):
    vehicle = Vehicle.objects.get(vehicle_id=pk)
    form = VehicleForm(instance=vehicle)

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request,"Vehicle updated succesfully")
            return redirect('vehicles-individual', pk=pk)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form,'vehicle':vehicle}
    return render(request,'main/admin/admin-vehicle-edit.html',context)

def admin_announcements(request):
    announcements = Announcement.objects.all()
    context = {'announcements':announcements}
    return render(request,'main/admin/admin-announcements.html',context)

def admin_announcements_individual(request,pk):
    announcement = Announcement.objects.get(title = pk)
    context = {'announcement':announcement}
    return render(request,'main/admin/admin-announcements-individual.html',context)

def admin_announcements_edit(request,pk):
    
    announcement = Announcement.objects.get(title = pk)
    form = AnnouncementForm(instance=announcement)
    if request.method == "POST":
        form = AnnouncementForm(request.POST,instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('admin-anncmnts-indiv', pk=pk)
    context = {'announcement':announcement,'form':form}
    return render(request,'main/admin/admin-announcements-edit.html',context)

def admin_announcements_delete(request,pk):
    announcement = Announcement.objects.get(title = pk)
    
    if request.method == "POST":
        announcement.delete()
        return redirect('admin-anncmnts')
    context = {'announcement':announcement}
    return render(request,'main/admin/admin-announcements-delete.html',context)