from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse, FileResponse
from .models import User,DriverPayment,DriverFeedback,DriverStudents,Schedule,Franchise,VehicleRequest,VehicleUpdateRequest,Profile,FranchiseDrivers,Driverprofile,Reservation,Announcement,ReservationCancelation,Vehicle,Services,Payment,Accounts
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from .forms import VehicleUpdateForm,ServiceRegister,AdminFranchiseDriversDocs,AdmineditStudent,FranchiseDocs,DriverPaymentProof,CHOICES,DriverFeedbackForm,PickUpTimeForm,ScheduleForm,adminFranchiseRegistrationForm,ServicesForm,AdminVehicleForm,VehicleForm,FranchiseDriversForm,FranchiseRegistrationForm,ReservationForm,Proof_of_payment,NotAdminDriverProfileForm, NotAdminDriverUserForm,FranchiseForm,AnnouncementForm,VehicleForm,ReservationEditForm,AdminEditDriverProfileForm, GroupAdminForm,CancelationForm,DriverProfilePicture,EditProfileForm,SetPasswordForm,PasswordResetForm,EditUserForm,ProfileForm,ProfilePicture,DriverProfileForm,StudentUserForm,DriverUserForm
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
from django.utils.crypto import get_random_string
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

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

def activateEmailDriver(request,franchise,password, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("main/driver_activate_account.html", {
        'user': user.email,
        'driver':user,
        'pass':password,
        "franchise":franchise,
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
    return render(request,'main/forgot-pas.html', context)

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
#delete mo to

def student_myservice(request):
    reservations = Reservation.objects.filter(active=True, user = request.user)
    payments = Payment.objects.filter(user = request.user)
    
    
    if reservations and payments:
        today = datetime.date.today()
        year = today.strftime("%Y")
        account = Accounts.objects.get(user = request.user)
        payments = Payment.objects.filter(account= account)
        entry = DriverStudents.objects.get(student = request.user.profile) 
        reservation = Reservation.objects.filter(user = request.user,reservation_status = "SUCCESSFULL")
        
        
        
        
        for r in reservation:
            if str(r.get_year()) == str(year):
                x = r.reservation_id
        reserve = Reservation.objects.get( reservation_id = x)
        total = 0
        for p in payments:
            total = p.total + total
    else:
       return redirect('reservation')
        

    context={'entry':entry, 'reserve':reserve, 'total':total}
    return render(request,'main/student/student_my_service.html',context)

def student_driver_feedback(request,pk):
    driver = Driverprofile.objects.get(user_id = pk)
    form = DriverFeedbackForm()
    rdio = CHOICES()
    
    if request.method == "POST":
        rdio = CHOICES(request.POST)
        form = DriverFeedbackForm(request.POST)
        
        
        if form.is_valid() and rdio.is_valid():
            selected = rdio.cleaned_data.get("NUMS")
            feedback = form.save(commit=False)
            feedback.driver = driver
            feedback.user = request.user
            feedback.rate = selected
            feedback.save()
            
            messages.success(request,"Feedback submitted, thank you for your response.")
            return redirect('myservice')
    context = {'form':form, 'rdio':rdio}
    return render(request,'main/student/driver-feedback.html',context)
    


def student_payments(request,pk):
    months = ["September","October","November","December","January","February","March","April","May","June"]
    account = Accounts.objects.get(acct_no = pk)
    payment = Payment.objects.get(ref_no=pk)
    context={'months':months,'payment':payment}
    return render(request,'main/student/payments.html',context)

def profile_fillUp(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile updated succesfully")
            return redirect('sched-fill')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form}
    return render(request,'main/student/student_profile_form.html',context)
def schedule(request):
    pass
def schdeule_fillup(request):
    sched_tb = Schedule.objects.get(student = request.user.profile)
    form = ScheduleForm(instance = sched_tb)
    if request.method == "POST":
        form = ScheduleForm(request.POST,instance = sched_tb)
        if form.is_valid():
            form.save()
            messages.success(request,'Schedule successfully submited')
            return redirect('navPage')
    context={'form':form}
    return render(request,'main/student/student_schedule_form.html',context)
@unauthenticated_user
def login_page(request):
    reservations = Reservation.objects.all()
    
    for r in reservations:
        if r.created < r.valid_until:
            r.active =False    
            
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
                elif user.is_franchise:
                    return redirect('franchise-nav')
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
       
        TnA = request.POST.get('tna')
        if form.is_valid() and TnA == "agree":
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.is_student=True
            user.role = "STUDENT"
            group = Group.objects.get(name='student')
            
            user.save()
            user.groups.add(group)
            acct = Accounts.objects.create(user = user)
            acct.save()
            
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('navPage')
        else:
            if TnA != "agree":
                messages.error('please acknowledge terms and conditions')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
    context = {'form':form}
    return render(request,'main/student/student_registration_page.html' ,context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def mainNavPage(request):   
   
    return render(request,'main/student/student_navigation_page.html')

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
    guard = True
    profile = Profile.objects.get(user = request.user)
    
    address = []
    address.append(profile.lot)
    address.append(profile.street)
    address.append(profile.village)
    
    
    reservations = Reservation.objects.filter(user = request.user,reservation_status="SUCCESSFULL",active = True)
    

    if reservations:
        return redirect('cancel-reserve')
             
    services = Services.objects.filter(status = "APPROVED")
    
    available = []
    for s in services:
        if s.pick_up in address:
            available.append(s)

    if not available:
        guard = False
    context={'services':services, 'available':available,'guard':guard}
    return render(request,'main/student/reservation_driver_list.html',context)

def existing_reservation(request):
    reservations = Reservation.objects.filter(user = request.user,reservation_status="SUCCESSFULL")
    
    today = datetime.date.today()
    year = today.year
    
    
    context = {'reservations':reservations,'year':year}
    return render(request,'main/student/reservation_not_confirmed.html',context)

def waiting_cancelation(request):
    return render(request,'main/waiting-cancelation.html')
    
def reservation_driver_info(request,pk):
    
    service = Services.objects.get(service_id=pk)
    profile_driver = service.driver
    
    if request.method == "POST":
        reservation = Reservation.objects.create(user = request.user , driver = service.driver, service = service )
        reservation.valid_until =  reservation.created.date() + datetime.timedelta(days=1)
        reservation.save()
        mssg = f'hi{reservation.user.last_name}, your reservation has been recorded plesase wait for the confirmation of your reservation', 
        reservation.send_sms(mssg)
        messages.success(request,"We received your reservation, please wait for the confimation email")
        return redirect('navPage')
    context={'service':service,'profile_driver': profile_driver}
    return render(request,'main/reservation/reservation_driver_profile.html',context)




    
    

    
#Student views ends here....


#Driver views....
@login_required(login_url='login')
@allowed_users(allowed_roles=['driver','admin'])
def driver_profile_fillUp(request):
    form = DriverProfileForm()
    franchise = FranchiseDrivers.objects.get(driver=request.user)
    if request.method == 'POST':
        form = DriverProfileForm(request.POST, request.FILES,instance=request.user.driverprofile)
       
        if form.is_valid() :
            request.user.driverprofile.franchise = franchise.franchise
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

def driver_myservice(request):
    today = datetime.datetime.now()
    #dow = today.strftime('%A')
    dow = "Monday"
    drvr_stdnt_table = DriverStudents.objects.filter(assigned_driver = request.user)
    context = {'table':drvr_stdnt_table,'dow':dow}

    return render(request,'main/driver/driver_myservice.html',context)

def driver_add_pickup_time(request,pk):
    profile = Profile.objects.get(user_id = pk)
    drvr_stdnt_table = DriverStudents.objects.filter(assigned_driver = request.user)
    form = PickUpTimeForm(instance = profile)
    
    if request.method == "POST":
        form = PickUpTimeForm(request.POST,instance = profile.schedule)
        if form.is_valid():
            sched = form.save()
           
            messages.success(request,"Data successfully submitted")
            current_date = datetime.datetime.now()  
            subject = 'ReService:School Service Reservation'
            message = render_to_string("main/pickup_mssg.html", {
                                'profile': profile,
                                'sched':sched,
                                'date':current_date,
                    
                            })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[profile.user.email], fail_silently=False)
    
            mssg = f'hi{profile.user.last_name}, your driver has set pick up time for you, kindly check your email', 
            profile.send_sms(mssg)
            return redirect('myservice-driver')
            
    context = {'table':drvr_stdnt_table,"form":form,'profile':profile}
    return render(request,'main/driver/driver_set_pickup.html',context)
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

@login_required(login_url='login')
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
def admin_feedbacks(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    franchise_list = Franchise.objects.values_list('franchise_name',flat=True).distinct()
    feedbacks = DriverFeedback.objects.filter(
        Q(rep_id__icontains = q)|
        Q(driver__user__last_name__icontains = q)|
        Q(driver__user__first_name__icontains = q)|
        Q(driver__user__middle_name__icontains = q)|
        Q(user__last_name__icontains = q)|
        Q(user__first_name__icontains = q)|
        Q(user__middle_name__icontains = q)|
        Q(rate__icontains = q)|
        Q(concern__icontains = q)
    )
    
    context={'feedbacks':feedbacks,'franchise_list':franchise_list}
    return render(request,'main/admin/admin_feedbacks.html',context)

def admin_feedback_indiv(request,pk):
    feedback = DriverFeedback.objects.get(rep_id = pk)
    context = {'feedback':feedback}
    return render(request,'main/admin/admin_feedbacks_indiv.html',context)

def admin_notify_feedback(request,pk):
    feedback = DriverFeedback.objects.get(rep_id = pk)
    current_date = datetime.datetime.now()  
    subject = 'ReService: Driver Evaluation'
    message = render_to_string("main/notify_feedback_mssg.html", {
                            'feedback': feedback,                        
                            'date':current_date,
                          
                        })
        
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from,[feedback.driver.franchise.email], fail_silently=False)
    messages.success(request,'EMail sent successfully')
    return redirect('feedback-indiv',pk=pk)

"""  q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(
        Q(user__last_name__icontains = q)|
        Q(user__first_name__icontains = q)|
        Q(user__middle_name__icontains = q)|
        Q(id__icontains = q)
    )
    reservations = Reservation.objects.filter(
        Q(reservaiton_id__icontains = q)|
        Q(user__last_name__icontains = q) |
        Q(user__first_name__icontains = q) |
        Q(reservation_status__icontains = q)
    )
    payments = Payment.objects.filter(
        Q(ref_no__icontains =  q)|
        Q(user__last_name__icontains =  q)|
        Q(user__first_name__icontains =  q)|
        Q(user__middle_name__icontains =  q)|
        Q(ref_no__icontains =  q)|
        Q(account__acct_no__icontains = q)|
        Q(reservation__reservation_id__icontains =  q)|
        Q(total__icontains =  q)|
        Q(created__icontains =  q)
    """
    
def admin_reports(request):
    users = User.objects.all()
    reservations = Reservation.objects.all()
    payments = Payment.objects.all()
    if request.method == "POST":
        print = request.POST.get('print')
        
        if print == "resmonth":
            return redirect('print-pdf-resmonth')
        elif print =="resyear":
            return redirect('pdf-yearly')
        elif print =="resall":
            return redirect('pdf-all-res')
        elif print =="payall":
            return redirect('pdf-payments-all-rprt')
        elif print == "paymonth":
            return redirect('monthly-payments')
        elif print == "payyear":
            return redirect('yearly-payments-report')
        elif print == "userall":
            return redirect('pdf-users-all')
        elif print == "all":
            return redirect('all')
    
    context={'reservations':reservations,'payments':payments,'users':users}
    return render(request,'main/admin/admin_reports.html',context)

def all_report(request):
    users = User.objects.all()
    payments = Payment.objects.all()
    reservations = Reservation.objects.all()
    template_path = 'main/all_report.html'
    today = datetime.datetime.now()

    
    user_count = len(users)
    payments_count = len(payments)
    reservation_count = len(reservations)
    
    bank = []
    
    for p in payments:
        bank.append(p.total)
    
    total = 0.0
    for p in bank:
        total = float(total) + float(p)
    
    context = {'users':users,
               'payments':payments,
               'reservations':reservations,
               'today':today,
               'user_count':user_count,
               'payments_count':payments_count,
               'reservation_count':reservation_count,
               'total':total
               
                   
                   }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
def render_pdf_user_all(request):
    template_path = 'main/user_all_report.html'
    today = datetime.datetime.now()

    users = User.objects.all()
    student_users = User.objects.filter(role = "STUDENT")
    driver_users = User.objects.filter(role="DRIVER")
    franchise_users = User.objects.filter(role = "FRANCHISE")
    
    user_count = len(users)
    student_count = len(student_users)
    franchise_count = len(franchise_users)
    driver_count = len(driver_users)
    
    context = {'users':users,
               'student_users':student_users,
               'driver_users':driver_users,
               'franchise_users':franchise_users,
               'today':today,
               'user_count':user_count,
               'student_count':student_count,
               'franchise_count':franchise_count,
               'driver_count':driver_count
               
                   
                   }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def render_pdf_payment_yearly(request):
    template_path = 'main/payments_yearly_report.html'
    today = datetime.datetime.now()   
    year = today.strftime("%Y")
    
    payments = Payment.objects.all()
    unsuccessfull_payment = Payment.objects.filter(status = "FAILED")
    pending_payment = Payment.objects.filter(status="PENDING")
    successful_payment = Payment.objects.filter(status = "SUCCESSFULL")
    
   
    bank = []
    monthly_pay = []
    unsuccessfull_monthly = []
    successfull_monthly = []
    pending_monthly = []
    for p in payments:
        if str(p.get_year()) == str(year):
            monthly_pay.append(p)
    
    for p in unsuccessfull_payment:
        if str(p.get_year()) == str(year):
            unsuccessfull_monthly.append(p)
            
    for p in successful_payment:
        if str(p.get_year()) == str(year):   
            successfull_monthly.append(p)
    
    for p in pending_payment:
        if str(p.get_year()) == str(year):   
            pending_monthly.append(p)
            
            
    for p in successfull_monthly:
        bank.append(p.total)

    total = 0.0
    for m in bank:
        total = total + float(m)
    
    unsuccessfull_payment_count = len(unsuccessfull_monthly)
    pending_payment_count = len(pending_monthly)
    payments_count = len(monthly_pay)
    successful_payment_count = len(successfull_monthly )
          
    
    context = {'payments':monthly_pay,
               'unsuccessfull_payment_count':unsuccessfull_payment_count,
               'pending_payment_count':pending_payment_count,
               'payments_count':payments_count,
               'today':today,
               'successful_payment_count':successful_payment_count,
               'total':total,
               'month':year
               
                   
                   }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def render_pdf_payment_month(request):
    template_path = 'main/payments_monthly_report.html'
    today = datetime.datetime.now()   
    month = today.strftime("%B")
    
    payments = Payment.objects.all()
    unsuccessfull_payment = Payment.objects.filter(status = "FAILED")
    pending_payment = Payment.objects.filter(status="PENDING")
    successful_payment = Payment.objects.filter(status = "SUCCESSFULL")
    
   
    bank = []
    monthly_pay = []
    unsuccessfull_monthly = []
    successfull_monthly = []
    pending_monthly = []
    for p in payments:
        if str(p.get_month()) == str(month):
            monthly_pay.append(p)
    
    for p in unsuccessfull_payment:
        if str(p.get_month()) == str(month):
            unsuccessfull_monthly.append(p)
            
    for p in successful_payment:
        if str(p.get_month()) == str(month):   
            successfull_monthly.append(p)
    
    for p in pending_payment:
        if str(p.get_month()) == str(month):   
            pending_monthly.append(p)
            
            
    for p in successfull_monthly:
        bank.append(p.total)

    total = 0.0
    for m in bank:
        total = total + float(m)
    
    unsuccessfull_payment_count = len(unsuccessfull_monthly)
    pending_payment_count = len(pending_monthly)
    payments_count = len(monthly_pay)
    successful_payment_count = len(successfull_monthly )
          
    
    context = {'payments':monthly_pay,
               'unsuccessfull_payment_count':unsuccessfull_payment_count,
               'pending_payment_count':pending_payment_count,
               'payments_count':payments_count,
               'today':today,
               'successful_payment_count':successful_payment_count,
               'total':total,
               'month':month
               
                   
                   }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def render_pdf_payment_all(request):
    template_path = 'main/payments_all_report.html'
    today = datetime.datetime.now()

    payments = Payment.objects.all()
    unsuccessfull_payment = Payment.objects.filter(status = "FAILED")
    pending_payment = Payment.objects.filter(status="PENDING")
    successful_payment = Payment.objects.filter(status = "SUCCESSFULL")
    unsuccessfull_payment_count = len(unsuccessfull_payment)
    pending_payment_count = len(pending_payment)
    payments_count = len(payments)
    successful_payment_count = len(successful_payment )
    bank = []
    
    for p in successful_payment:
        bank.append(p.total)
    
    total = 0.0
    for m in bank:
        total = total + float(m)
        
          
    
    context = {'payments':payments,
               'unsuccessfull_payment_count':unsuccessfull_payment_count,
               'pending_payment_count':pending_payment_count,
               'payments_count':payments_count,
               'today':today,
               'successful_payment_count':successful_payment_count,
               'total':total
               
                   
                   }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf_all(request):
    template_path = 'main/reservaiton_all_report.html'
    today = datetime.datetime.now()
    reservation = Reservation.objects.all()
    pending_reservations = Reservation.objects.filter(reservation_status = "PENDING")
    unpaid_reservations = Reservation.objects.filter(payment_status = "PENDING")
    

                
    count = len(reservation)
    pending_reservations_count = len(pending_reservations)
    unpaid_reservation_count = len(unpaid_reservations)
    
    context = {
               'reservation':reservation,
                'today':today,
                'count':count,
                'pending_reservations_count':pending_reservations_count,
                'unpaid_reservation_count':unpaid_reservation_count,
                   
                   }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_view_yearly(request):
    template_path = 'main/yearly_report.html'
    today = datetime.datetime.now()
    year = today.strftime("%Y")
    year_list = []
    unpaid_list_yearly=[]
    pending_list_yearly=[]
    reservation = Reservation.objects.all()
    pending_reservations = Reservation.objects.filter(reservation_status = "PENDING")
    unpaid_reservations = Reservation.objects.filter(payment_status = "PENDING")
    
    for r in reservation:
        if str(r.get_year()) == str(year):
            year_list.append(r)

    for r in pending_reservations:
        if str(r.get_year()) == str(year):
            pending_list_yearly.append(r)
        
    for r in unpaid_reservations:
        if str(r.get_year()) == str(year):
            unpaid_list_yearly.append(r)
                
    count = len(year_list)
    pending_reservations_count = len(pending_list_yearly)
    unpaid_reservation_count = len(unpaid_list_yearly)
    
    context = {'year':year,
               'reservation':year_list,
                'today':today,
                'month':year,
                'count':count,
                'pending_reservations_count':pending_reservations_count,
                'unpaid_reservation_count':unpaid_reservation_count,
                   
                   }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_view(request):
    template_path = 'main/reports.html'
    today = datetime.datetime.now()
    month1 = today.strftime("%B")
    month_list = []
    unpaid_list=[]
    pending_list=[]
    reservation = Reservation.objects.all()
    pending_reservations = Reservation.objects.filter(reservation_status = "PENDING")
    unpaid_reservations = Reservation.objects.filter(payment_status = "PENDING")
    for r in reservation:
        if str(r.get_month()) == str(month1):
            month_list.append(r)

    for r in pending_reservations:
        if str(r.get_month()) == str(month1):
            pending_list.append(r)
        
    for r in unpaid_reservations:
        if str(r.get_month()) == str(month1):
            unpaid_list.append(r)
                
    count = len(month_list)
    pending_reservations_count = len(pending_list)
    unpaid_reservation_count = len(unpaid_list)
    
    
    
    context = {'reservation':month_list,
                    'today':today,
                    'month':month1,
                    'count':count,
                    'pending_reservations_count':pending_reservations_count,
                    'unpaid_reservation_count':unpaid_reservation_count,
                   
                   }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def admin_payment_request(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    payments = Payment.objects.filter(
        Q(ref_no__icontains =  q)|
        Q(user__last_name__icontains =  q)|
        Q(user__first_name__icontains =  q)|
        Q(user__middle_name__icontains =  q)|
        Q(ref_no__icontains =  q)|
        Q(account__acct_no__icontains = q)|
        Q(reservation__reservation_id__icontains =  q)|
        Q(total__icontains =  q)|
        Q(created__icontains =  q)
        
        
    )
    context = {'payments':payments}
    return render(request,'main/admin/admin_payments.html',context)

def admin_driver_payments_request(request):
    pass

def admin_payments_indiv(request,pk):
    payment = Payment.objects.get(ref_no = pk)
    pay_reservation = payment.reservation
    reservation = Reservation.objects.get(reservation_id = pay_reservation.reservation_id)
    account = Accounts.objects.get(user = reservation.user)
    drv = DriverStudents.objects.all()
        
        
            
    reservation.valid_until = reservation.created.date() + datetime.timedelta(days=366)
    reservation.save()
    
    if request.method == "POST":
        payment.status = "SUCCESSFULL"
        account.balance = float(account.balance) - float(payment.total)
        account.save()
        reservation.payment_status = "PAID"
        reservation.save()
        payment.save()
        if str(payment.user.profile) not in str(drv):
            DriverStudents.objects.create(student = payment.user.profile, assigned_driver = reservation.driver.user)
            
            current_date = datetime.datetime.now()  
            subject = 'ReService:Payment Verification'
            message = render_to_string("main/payment_verified_mssg.html", {
                                'user': payment.user,
                                'reservation':payment.reservation,
                            
                                'date':current_date,
                                'payment':payment,
                            })
            
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[payment.user.email], fail_silently=False)
        messages.success(request,'Payment approved')
        return redirect('admin-payments')
    context={'payment':payment}
    return render(request,'main/admin/admin-payments-indiv.html',context)

def admin_payments_decline(request,pk):
    payment = Payment.objects.get(ref_no = pk)
   

    if request.method == "POST":
        payment.status = "DECLINED"
        payment.save()
        current_date = datetime.datetime.now()  
        subject = 'ReService:Payment Verification'
        message = render_to_string("main/payment_declined_mssg.html", {
                            'user': payment.user,
                            'reservation':payment.reservation,
                        
                            'date':current_date,
                            'payment':payment,
                        })
        
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from,[payment.user.email], fail_silently=False)
        
    context={'payment':payment}
    return render(request,'main/admin/admin-payments-decline.html',context)

def admin_nav_page(request):
    return render(request,'main/admin/admin_navigation.html')

def admin_franchise_users(request):
    franchise_list = Franchise.objects.values_list('franchise_name',flat=True).distinct()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    franchises = Franchise.objects.filter(
        Q(franchise_name__icontains = q)|
        Q(user__last_name__icontains = q)|
        Q(user__first_name__icontains = q)|
        Q(user__middle_name__icontains = q)|
        Q(driverprofile__franchise__franchise_name__icontains = q)|
        Q(user__email__icontains = q)|
        Q(driverprofile__lot__icontains = q)|
        Q(driverprofile__street__icontains = q)|
        Q(driverprofile__village__icontains = q)|
        Q(driverprofile__zipcode__icontains = q)|
        Q(driverprofile__city__icontains = q)
        ,franchise_status = "APPROVED")
    context={'franchises':franchises,'franchise_list':franchise_list}
    return render(request,'main/admin/admin-franchise-users.html',context)

def admin_franchise_users_edit(request,pk):
    owner = User.objects.get(id = pk)
    franchise = Franchise.objects.get(user = owner)
    
    form = NotAdminDriverUserForm(instance=owner)
    form_p =FranchiseDocs(instance=franchise)
    
    if request.method == "POST":
        form = NotAdminDriverUserForm(request.POST, instance=owner)
        form_p =FranchiseDocs(request.POST,request.FILES, instance = franchise) 
        if form.is_valid() and form_p.is_valid():
            form.save()
            form_p.save()
            messages.success(request, 'Changes applied successfully')
            return redirect('indiv-franchise-users', pk=pk)
    context = {'franchise':franchise,'form':form,'owner':owner,'form_p':form_p}
    return render(request,'main/admin/admin-franchise-users-edit.html',context)


def admin_franchise_delete(request,pk):
    franchise_user = User.objects.get(id = pk)
    
    if request.method == "POST":
        franchise_user.delete()
        messages.success(request, "Franchise Deleted Successfully")
        return redirect('add-franchise-users')
    context = {'franchise_user':franchise_user}
    return render(request,'main/admin/admin-franchise-users-delete.html',context)
    

def admin_register_franchise(request):
    form = FranchiseRegistrationForm()
    if request.method == 'POST':
        form = FranchiseRegistrationForm(request.POST)
        if form.is_valid() :
            form.save()
            
            messages.success(request,'Franchise Successfully Registered')
            return redirect('identify')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    context = {'form':form}
    return render(request,'main/franchise/franchise-register.html', context)

def admin_franchiser_users_indiv(request,pk):
    owner = User.objects.get(id = pk)
 
    franchise = Franchise.objects.get(user=owner)
    drivers = Driverprofile.objects.filter(franchise = franchise)
    vehicles = Vehicle.objects.filter(franchise=franchise)
    myDrivers = FranchiseDrivers.objects.filter(franchise = franchise, status= "APPROVED")
    context={'franchise':franchise,'myDrivers':myDrivers,'owner':owner,'vehicles':vehicles,'drivers':drivers}
    return render(request,'main/admin/admin_franchise_users_indiv.html',context)


def admin_franchise(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    franchise = Franchise.objects.filter(
        Q(franchise_name__icontains = q)|
        Q(franchise_no__icontains = q)|
        Q(operator_lastN__icontains = q)|
        Q(operator_firstN__icontains = q)|
        Q(operator_middleN__icontains = q)|
        Q(franchise_status__icontains = q)|
        Q(email__icontains = q)
        
    )
    context={'franchise':franchise}
    return render(request,'main/admin/admin-franchise.html',context)

def admin_franchise_indiv(request,pk):
    paasswrd = get_random_string(length=16)
    franchise = Franchise.objects.get(franchise_id = pk)
    approved_franchise = Franchise.objects.filter(franchise_status = "APPROVED")
    if request.method == "POST":
        if franchise in approved_franchise:
            messages.error(request,'franchise already approved')
        else:
            franchise = Franchise.objects.get(franchise_id = pk)
            franchise.franchise_status = "APPROVED"
            
            franchise.save()
            user = User.objects.create_user(email = franchise.email, password =paasswrd,contact_no = franchise.contact_no,last_name = franchise.operator_lastN, middle_name = franchise.operator_middleN, first_name = franchise.operator_firstN)
            user.is_franchise = True
            user.save()
            franchise.user = user
            franchise.save()
            user.is_active = True
            user.is_franchise=True
            user.role = "FRANCHISE"                               
            group = Group.objects.get(name='franchise')
                    
            user.save()
            user.groups.add(group)
        
            current_date = datetime.datetime.now()  
            
            subject = 'ReService: Franchise Registration'
            message = render_to_string("main/accept-franchise-mssg.html", {
                                'franchise': franchise,
                                'date':current_date,
                                'pass':paasswrd
                                
                            })
            email_from = settings.EMAIL_HOST_USER
            
            send_mail(subject, message, email_from,[franchise.email], fail_silently=False)
            messages.success(request,'Franchise approved')
            franchise.send_sms(f"Hello {franchise.user}, your franchise has been approved, for your account information ,please look into your registered email ")
            return redirect('admin-franchise')
    context={'franchise':franchise,}
    return render(request,'main/admin/admin-indiv-franchise.html',context)

def admin_franchise_add(request):
    paasswrd = get_random_string(length=16)
    form = FranchiseRegistrationForm()
    if request.method == 'POST':
        form = FranchiseRegistrationForm(request.POST)
        if form.is_valid() :
            form.save()
            franchise = form.save(commit=False)
            user = User.objects.create_user(email = franchise.email, password = paasswrd,contact_no = franchise.contact_no,last_name = franchise.operator_lastN, middle_name = franchise.operator_middleN, first_name = franchise.operator_firstN)
            
            user.role = "FRANCHISE"  
            user.is_active = True
            user.save()
            franchise.user = user
            franchise.save()
            user.is_franchise=True                              
            group = Group.objects.get(name='franchise')
                    
            user.save()
            user.groups.add(group)
            current_date = datetime.datetime.now()  
        
            subject = 'ReService: Franchise Registration'
            message = render_to_string("main/accept-franchise-mssg.html", {
                                'franchise': franchise,
                                'date':current_date,
                                'pass':paasswrd,
                                
                            })
            email_from = settings.EMAIL_HOST_USER
            
            send_mail(subject, message, email_from,[franchise.email], fail_silently=False)
            messages.success(request,'Franchise created successfully')
            franchise.send_sms(f"Hello {franchise.user}, your franchise has been approved, for your account information ,please look into your registered email ")
            return redirect('admin-franchise')
            
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    context = {'form':form}
    return render(request,'main/franchise_registration.html',context)
"""def admin_franchise_delete(request,pk):
    pass"""
def admin_franchise_decline(request,pk):
    franchise = Franchise.objects.get(franchise_id = pk)
    if request.method == "POST":
        franchise = Franchise.objects.get(franchise_id = pk)
        franchise.franchise_status = "DECLINED"
        
        franchise.save()
       
    
        current_date = datetime.datetime.now()  
        
        subject = 'ReService: Franchise Registration'
        message = render_to_string("main/franchise_decline_mssg.html", {
                            'franchise': franchise,
                            'date':current_date,
                            
                        })
        email_from = settings.EMAIL_HOST_USER
        
        send_mail(subject, message, email_from,[franchise.email], fail_silently=False)
        messages.success(request,'Franchise approved')
        franchise.send_sms(f"Hello {franchise.user}, we regret to inform you that your franchise request has been declined, for more information or inquiries contact ReService ")
        return redirect('admin-franchise')
    context={'franchise':franchise}
    return render(request,'main/admin/admin_franchise_decline.html',context)

def admin_franchise_driver_reqs(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    requests = FranchiseDrivers.objects.filter(
        Q(driver_code__icontains = q)|
        Q(franchise__franchise_name__icontains = q)|
        Q(driver_last_name__icontains = q)|
        Q(driver_first_name__icontains = q)|
        Q(driver_middle_name__icontains = q)|
        Q(status__icontains = q) |
        Q(email__icontains = q)
       
        
        
    )
    
    context = {'requests':requests}
    return render(request,'main/admin/admin_franchise_requests.html', context)

def admin_franchise_driver_reqs_indiv(request,pk):
    
    requests = FranchiseDrivers.objects.get(driver_code = pk)
    approved_reqs = FranchiseDrivers.objects.filter(status = "APPROVED")
    if request.method == "POST":
    

        if requests in approved_reqs:
            messages.error(request,"driver already approved")
            return redirect('driver-requests-admin')
            
        else:
            requests.status = "APPROVED"
            requests.save()
            
            
            driver_pay = DriverPayment.objects.create(driver = requests, total=3000, franchise = requests.franchise)
            current_date = datetime.datetime.now()  
            
            subject = 'ReService: Driver Franchise Registration'
            message = render_to_string("main/driver_franchise_accept_mssg.html", {
                                'requests': requests,
                                'date':current_date,
                                'driver_pay':driver_pay,
                                
                            })
            email_from = settings.EMAIL_HOST_USER
            
            send_mail(subject, message, email_from,[requests.franchise.user.email], fail_silently=False)
            messages.success(request,'Requests Approved')
            return redirect('driver-requests-admin')
    context = {'request':requests}
    return render(request,'main/admin/admin_franchise_requests_indiv.html', context)

def admin_driver_membership_payments(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    driver_payments = DriverPayment.objects.filter(
        Q(status__icontains = q)|
        Q(driver__driver_last_name__icontains = q)|
        Q(driver__driver_first_name__icontains = q)|
        Q(driver__driver_middle_name__icontains = q)|
        Q(total__icontains = q)|
         Q(created__icontains = q)
    )
    context = {'driver_payments':driver_payments}
    return render(request,'main/admin/admin_membership_payments.html', context)

def admin_driver_membership_payments_indiv(request,pk):
    payment = DriverPayment.objects.get(ref_no = pk)
    pwrd = get_random_string(length=16)
    requests = FranchiseDrivers.objects.get(driver_code = payment.driver.driver_code)
    if request.method == "POST":
        payment.status == "SUCCESSFULL"
        payment.save()
        
        requests.payment_status = "SUCCESSFULL" 
        requests.save()
        driver_user = User.objects.create_user(email=requests.email,password=pwrd,last_name= requests.driver_last_name,first_name = requests.driver_first_name, middle_name=requests.driver_middle_name, contact_no =requests.contact_no)
        driver_user.role = "DRIVER"
        driver_user.is_driver=True
        dprofile = Driverprofile.objects.create(user = driver_user, franchise = requests.franchise,vehicle = requests.vehicle )
        group = Group.objects.get(name='driver')
        driver_user.save()
        driver_user.groups.add(group)
            
        requests.driver = driver_user
        requests.save()
            
        activateEmailDriver(request, requests, pwrd, driver_user, driver_user.email)
        current_date = datetime.datetime.now()  
        
        subject = 'ReService: Driver Franchise Registration'
        message = render_to_string("main/driver_membership_verified_mssg.html", {
                                'payment': payment,
                                'requests':requests,
                                'pwrd':pwrd,
                            })
        email_from = settings.EMAIL_HOST_USER
            
        send_mail(subject, message, email_from,[requests.email], fail_silently=False)
        messages.success(request,'Requests Approved')
        return redirect('driver-requests-admin')
    context = {'payment':payment}
    return render(request,'main/admin/admin-membership-payments-indiv.html',context)

def admin_membership_payments_decline(request,pk):
    context={}
    return render(request,'main/admin/admin-membership-decline.html',context)

def franchise_driver_membership_pay(request):
    driver = FranchiseDrivers.objects.filter(franchise = request.user.franchise)
    driver_payments = DriverPayment.objects.filter( franchise = request.user.franchise)
    context={'driver_payments':driver_payments, 'driver':driver}
    return render(request,'main/franchise/franchise-membership-payment.html', context)

def franchise_driver_membership_pay_indiv(request,pk):                               
    payment = DriverPayment.objects.get(ref_no = pk)
    
    context ={'payment':payment}
    return render(request,'main/franchise/franchise-membership-payment-indiv.html',context)

def membership_payment_pdf(request,pk):
    template_path = 'main/membership-fee-pdf.html'
    today = datetime.datetime.now()
    payment = DriverPayment.objects.get(ref_no = pk)

    
    context = {'payment':payment }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def franchise_membership_proof(request):
    driver_payments = DriverPayment.objects.filter(franchise = request.user.franchise)
    form = DriverPaymentProof()
    list = []
    for x in driver_payments:
        if x.status == "PENDING":
            list.append(x.ref_no)
  
    if request.method == "POST":
        ref = request.POST.get('ref')
      
        payment = DriverPayment.objects.get(ref_no = ref)
        form = DriverPaymentProof(request.POST,request.FILES, instance=payment)
        if form.is_valid():
            form.save()
      
            messages.success(request,'Proof of payment submitted, please wait for your payment verification')
            return redirect('membership')
        
    context={'driver_payments':driver_payments,'form':form,'list':list}
    return render(request,'main/franchise/franchise_membership_proof.html', context)

#admin services
def admin_services_requests(request):
    #admin-requests-services
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    services = Services.objects.filter(
        Q(service_id__icontains = q)|
        Q(price__icontains = q)|
        Q(pick_up__icontains = q)|
        Q(franchise__franchise_name__icontains = q)|
        Q(status__icontains = q)|
        Q(driver__user__last_name__icontains = q)|
        Q(driver__user__first_name__icontains = q)|
        Q(driver__user__middle_name__icontains = q)
    )
    context = {'services':services}
    
    return render(request,'main/admin/admin_services_requests.html', context)

def admin_services_requests_indiv(request,pk):
    #admin-requests-services
    service = Services.objects.get(service_id = pk)
    if request.method == "POST":
        service.status = "APPROVED"
        service.save()
        current_date = datetime.datetime.now()  
        
        subject = 'ReService: Driver Franchise Registration'
        message = "your service requ4est has been approved"
        email_from = settings.EMAIL_HOST_USER
        
        send_mail(subject, message, email_from,[service.franchise.user.email], fail_silently=False)  
        messages.success(request, 'Requests approved')
        return redirect('admin-requests-services')
    context = {'service':service}
    
    return render(request,'main/admin/admin_services_requests_indiv.html', context)

def admin_services_decline(request,pk):
    service = Services.objects.get(service_id = pk)
    
    if request.method == "POST":
        service.status = "DECLINED"
        service.save()
        current_date = datetime.datetime.now()  
        
        subject = 'ReService: Driver Franchise Registration'
        message = "your service request has been denied"
        email_from = settings.EMAIL_HOST_USER
        
        send_mail(subject, message, email_from,[service.franchise.user.email], fail_silently=False)  
        messages.success(request, 'Requests Denied')
        return redirect('admin-requests-services')
    context = {'service':service}
    
    return render(request,'main/admin/admin_services_requests_denied.html', context)
def admin_students(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(
        Q(id__icontains = q) |
        Q(last_name__icontains = q)|
        Q(first_name__icontains = q)|
        Q(middle_name__icontains = q)|
        Q(profile__section__icontains = q)|
        Q(profile__lot__icontains = q)|
        Q(profile__street__icontains = q)|
        Q(profile__village__icontains = q)|
        Q(profile__zipcode__icontains = q)|
        Q(profile__city__icontains = q)|
        Q(profile__year_level__icontains = q)|
        Q(reservation__reservation_status__icontains=q), role="STUDENT"
        
    )
    context = {'users':users}
    return render(request,'main/admin/admin-students.html',context)

def admin_create_student(request):
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
            
            acct = Accounts.objects.create(user = user)
            acct.save()
            
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('admin-nav')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    context = {'form':form}
    return render(request,'main/student/student_registration_page.html' ,context)
def admin_students_indiv(request,pk):
    userS = User.objects.get(id=pk)
    #reservation = Reservation.objects.get(user_id=pk)
    
    context = {'userS':userS,"reservation":reservation ,}
    return render(request,'main/admin/admin-student-individual.html',context)

def admin_student_edit(request,pk):
    user = User.objects.get(id=pk)
    profile_user= Profile.objects.get(user__id=pk)
    form = AdmineditStudent(instance=user)
    schedule = Schedule.objects.get(student =profile_user )
    pform=ProfilePicture(instance = profile_user)
    form_p=ProfileForm(instance=profile_user)
    form_s=ScheduleForm(instance = schedule)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        pform=ProfilePicture(request.POST, request.FILES, instance=profile_user)
        form_p= EditProfileForm(request.POST, request.FILES, instance=profile_user)
        form_s = ScheduleForm(request.POST, request.FILES, instance=schedule)
        if form.is_valid() and pform.is_valid() and form_p.is_valid() and form_s.is_valid():
            form.save()
            pform.save()
            form_p.save()
            form_s.save()
            messages.success(request,"Profile updated succesfully")
            return redirect('admin-stdnt-info', pk=pk)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form,'pform':pform, "profile_user":profile_user,'form_p':form_p,'form_s':form_s}
    return render(request,'main/admin/admin_student_edit.html',context)

def admin_student_delete(request,pk):
    user = User.objects.get(id=pk)
    
    if request.method == "POST":
        user.delete()
        return redirect('admin-students')
    context={'user':user}
    return render(request,'main/admin/admin_delete_user.html',context)


def admin_drivers(request):
    franchise_list = Franchise.objects.values_list('franchise_name',flat=True).distinct()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(
        Q(id__icontains = q) |
        Q(last_name__icontains = q)|
        Q(first_name__icontains = q)|
        Q(middle_name__icontains = q)|
        Q(driverprofile__franchise__franchise_name__icontains = q)|
        Q(email__icontains = q)|
        Q(driverprofile__lot__icontains = q)|
        Q(driverprofile__street__icontains = q)|
        Q(driverprofile__village__icontains = q)|
        Q(driverprofile__zipcode__icontains = q)|
        Q(driverprofile__city__icontains = q)
   
 
        , role="DRIVER"
        
    )
    context = {'users':users,'franchise_list':franchise_list}
    return render(request,'main/admin/admin_drivers.html',context)

def admin_add_driver(request):
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
            return redirect('admin-nav')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    context = {'form':form, 'page':page}
    return render(request,'main/driver/driver_registration_page.html', context)

def admin_drivers_indiv(request,pk):
    userS = User.objects.get(id=pk)
    reservation = Reservation.objects.filter(driver = userS.driverprofile,reservation_status = "SUCCESSFULL",active=True)
    #reservation = Reservation.objects.get(user_id=pk)
    
    context = {'userS':userS,"reservation":reservation ,}
    return render(request,'main/admin/admin-driver-individual.html',context)

def admin_driver_edit(request,pk):
    user = User.objects.get(id=pk)
    profile_user = Driverprofile.objects.get(user__id=user.id)
    form = DriverUserForm(instance=user)
    pform=DriverProfilePicture(instance=profile_user)
    form_p=AdminEditDriverProfileForm(instance=profile_user)
    frandriver = FranchiseDrivers.objects.get(driver = user)
    docForm = AdminFranchiseDriversDocs(instance = frandriver)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        form_p= AdminEditDriverProfileForm(request.POST, request.FILES, instance=profile_user)
        docForm = AdminFranchiseDriversDocs(request.POST, request.FILES,instance = frandriver)
        pform=DriverProfilePicture(request.POST, request.FILES,instance=profile_user)
        if form.is_valid() and form_p.is_valid() and docForm.is_valid() and pform.is_valid() :
            form.save()
            form_p.save()
            docForm.save()
            pform.save()
            messages.success(request,"Profile updated succesfully")
            return redirect('admin-drvr-info', pk=pk)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    context ={'form':form, "profile_user":profile_user,'form_p':form_p,'pform':pform,'user':user,'docForm':docForm}
    return render(request,'main/admin/admin_driver_edit.html',context)

def admin_reservation_deactivate(request):
    context = {}
    return render(request,'main/admin/admin_reservation_cancelation_real.html',context)

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

def admin_add_reservation(request):
    form = ReservationForm()
    
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('admin-reservations')
        
    context={'form':form}
    return render(request,'main/admin/admin_add_reservation.html',context)

def admin_reservation_indiv(request,pk):
    reservation = Reservation.objects.get(reservation_id=pk)
    
    if request.method == "POST":
        account = Accounts.objects.get(user = reservation.user)
        account.balance  = float(reservation.service.price)*10
        account.save()
        reservation.reservation_status = "SUCCESSFULL"
        reservation.active = True
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
    reservation = Reservation.objects.get(reservation_id = cancelation.reservation.reservation_id)
    if request. method == "POST":
        reservation.reservation_status = "DECLINED" 
        reservation.active = False
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
    context={'cancelation':cancelation}
    return render(request,'main/admin/admin_cancelation_individual.html', context)

def admin_cancelation_accept(request,pk):
    cancelation = ReservationCancelation.objects.get(cancelation_id = pk)
    reservation = Reservation.objects.get(reservation_id = cancelation.reservation.reservation_id)
    #reservation.delete()
   

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
    franchise_list = Franchise.objects.values_list('franchise_name',flat=True).distinct()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    vehicles = Vehicle.objects.filter(
        Q(vehicle__model__icontains = q) |
        Q(vehicle__plate_no__icontains = q) |
        Q(vehicle__franchise__franchise_name__icontains = q) |
        Q(vehicle__vehicle_id__icontains = q) 
  
    )
    franchise = Driverprofile.objects.values_list('franchise', flat=True)
    context = {'vehicles':vehicles,'int':int, 'franchise':franchise,'franchise_list':franchise_list}
    return render(request,'main/admin/admin_vehicles.html', context)

def admin_vehicles_individual(request,pk):
    vehicle = Vehicle.objects.get(vehicle = pk)
    
    context={'vehicle':vehicle}
    return render(request,'main/admin/admin_vehicles_individual.html', context)



def admin_vehicle_delete(request,pk):
    vehicle = Vehicle.objects.get(vehicle_id=pk)
    
    if request.method == "POST":
        vehicle.delete()
        return redirect('vehicles')
    context = {'vehicle':vehicle}
    return render(request,'main/admin/admin-vehicles-delete.html', context)

def admin_vehicle_add(request):
    form = AdminVehicleForm()
    if request.method == "POST":
        form = AdminVehicleForm(request.POST,request.FILES)
        
        if form.is_valid():
            vehicle = form.save()
            current_date = datetime.datetime.now()  
            subject = 'ReService:Vehicle Registration'
            message = render_to_string("main/vehicle_registation_mssg.html", {
                                'operator':vehicle.franchise.user,
                                'vehicle': vehicle.model,
                                'date':current_date,
                            })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[request.user.email], fail_silently=False)
            messages.success(request, 'request submittted')
            return redirect('vehicles')

    context = {'form':form}
    return render(request,'main/admin/admin-vehicles-add.html', context)


def admin_vehicle_edit(request,pk):
    vehicle = VehicleRequest.objects.get(vehicle_id=pk)
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


def admin_vehicle_request(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    vehicles = VehicleRequest.objects.filter(
        Q(model__icontains = q)|
        Q(franchise__franchise_name__icontains = q)|
        Q(plate_no__icontains = q)|
        Q(plate_no__icontains = q)|
        Q(status__icontains = q)
    )
    vehicleupdates = VehicleUpdateRequest.objects.all()
    context={'vehicles':vehicles,'vehicleupdates':vehicleupdates}
    return render(request,'main/admin/admin_vehicle_requests.html',context)

def admin_vehicle_updates_indiv(request,pk):

    vehicleupdates = VehicleUpdateRequest.objects.get(update_req=pk)
    vehicle = Vehicle.objects.get(vehicle_id = vehicleupdates.vehicle.vehicle_id)
    model = vehicle.model
    plate = vehicle.plate_no
    capacity = vehicle.capacity
    recit =  vehicle.OR
    cert = vehicle.CR
    if request.method == "POST":
        
        vehicle.status = "APPROVED"
        vehicleupdates.status = "APPROVED"
        vehicle.model = model
        vehicle.plate_no = plate
        vehicle.capacity = capacity
        vehicle.recit = recit
        vehicle.cert = cert
        vehicle.save()
        messages.success(request,'Changes successfully applied')
    context = {'vehicleupdates':vehicleupdates,'vehicle':vehicle,'model':model,'plate':plate,'capacity':capacity,'recit':recit,'cert':cert}
    return render(request,'main/admin/admin_vehicle_update_requests_indiv.html',context)
def admin_vehicle_request_indiv(request,pk):
    vehicle = VehicleRequest.objects.get(vehicle_id = pk)
    vehicle_approved = VehicleRequest.objects.filter(status="APPROVED")
    if request.method == "POST":
        
        
        if vehicle in vehicle_approved:
            messages.error(request,"vehicle already approved")
            return redirect('admin-vehicle-req')
        else:
            vehicle.status = "APPROVED"
            vehicle.save()
            approved_vehicle = Vehicle.objects.create(vehicle=vehicle, franchise=vehicle.franchise)
            current_date = datetime.datetime.now()  
            subject = 'ReService:School Service Reservation'
            subject = 'ReService:School Service Reservation Cancelation'
            message = render_to_string("main/approved_vehicle_mssg.html", {
                                'vehicle':vehicle,
                                'date':current_date,
                            })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[vehicle.franchise.user.email], fail_silently=False)
            messages.success(request,'Vehicle approved')
            return redirect('admin-vehicle-req')
    context = {'vehicle':vehicle
                }
    return render(request,'main/admin/admin_vehicle_requests_indiv.html',context)

def admin_vehicle_request_decline(request,pk):
    vehicle = Vehicle.objects.get(vehicle_id = pk)
    if request.method == "POST":
        vehicle.status = "DECLINED"
        vehicle.save()
        current_date = datetime.datetime.now()  
        subject = 'ReService:School Service Reservation'
        subject = 'ReService:School Service Reservation Cancelation'
        message = render_to_string("main/declined_vehicle_mssg.html", {
                            'vehicle':vehicle,
                            'date':current_date,
                        })
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from,[vehicle.franchise.user.email], fail_silently=False)
        messages.success(request,'Vehicle declined')
        return redirect('admin-vehicle-req')
    context={'vehicle':vehicle}
    return render(request,'main/admin/admin_vehicle_requests_decline.html',context)


def admin_announcements(request):
    list = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    announcements = Announcement.objects.filter(
        Q(created__icontains = q)|
        Q(title__icontains = q)
    
        
    )
    context = {'announcements':announcements,'list':list}
    return render(request,'main/admin/admin-announcements.html',context)


def admin_add_announcements(request):
    form = AnnouncementForm()
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-anncmnts')
    context={'form':form}
    return render(request, 'main/admin/admin_add_announcements.html',context)

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



#proof_of_payment
def submit_proof_of_payment(request,pk):
    account = Accounts.objects.get(user = request.user)
    reservation = Reservation.objects.get(reservation_id = pk)
    service = Services.objects.get(service_id = reservation.service.service_id)
    payment = Payment.objects.filter(account = account)
    form = Proof_of_payment()
    refs = []
    
    for p in payment:
        refs.append(p.ref_no)
    if request.method == "POST":
        
        
        user_ref = request.POST.get('ref')
        payment = Payment.objects.filter(account = account)
        
        if user_ref in str(payment):
            real_payment = Payment.objects.get(ref_no = user_ref)
            guard = True
            form = Proof_of_payment(request.POST, request.FILES, instance=real_payment)
            
        else:
            guard = False
        
        if guard == True and form.is_valid():
            form.save()
            messages.success(request, "Proof submitted successfully")
            return redirect('pay-reservation', pk = reservation.reservation_id)
        else:
            messages.error(request,"Reference no is not valid")
            return redirect('proof-payment', pk=pk)
            
    
    context={'account':account,'service':service,'payment':payment,'form':form,'reservation':reservation,'refs':refs}
    return render(request,'main/student/proof-pay.html',context)

def pay_reservation(request,pk):
    months = ["September","October","November","December","January","February","March","April","May","June"]
    account = Accounts.objects.get(user = request.user)
    #payment = Payment.objects.filter(account= account)
    reservation = Reservation.objects.get(reservation_id = pk)
    service = Services.objects.get(service_id = reservation.service.service_id)
    context={'months':months,'account':account,'service':service,'reservation':reservation}
    return render(request,'main/student/payments.html',context)

def payment(request,pk):
    period = ['1st Payment','2nd Payment','3rd Payment','4th Payment','5th Payment','6th Payment','7th Payment','8th Payment','9th Payment','10th Payment']
    total_payment = Payment.objects.filter(user = request.user, status ="SUCCESSFULL")
    total = 0.0
   
       
    account = Accounts.objects.get(user = request.user)
    reservation = Reservation.objects.get(reservation_id = pk)
    service = Services.objects.get(service_id = reservation.service.service_id)
    if total_payment:
        for money in total_payment:
            total = total + float(money.total)
        
        count = total / float(service.price)
        
        for i in reversed(range(1,int(count)+1)):
            period.pop(i-1)
            
    if request.method == "POST":
        total = 0.0
        #choice = request.POST.get('payment')
        price = request.POST.getlist('pay')

        for p in price:
            total =float(total) + float(p)
      
        user_payment = Payment.objects.create(user = request.user, account = account, reservation = reservation, total = total)
            
        return redirect('payment-summary', pk=user_payment.ref_no)
    context={'account':account,'service':service,'period':period}
    return render(request,'main/student/pay_balance.html',context)

def payment_summary(request,pk):
    account = Accounts.objects.get(user = request.user)
    payments = Payment.objects.get(ref_no= pk)
    reservation = Reservation.objects.get(reservation_id = payments.reservation.reservation_id)
    service = Services.objects.get(service_id = reservation.service.service_id)
    
    context={'account':account,'service':service, 'reservation':reservation,'payment':payments}
    return render(request,'main/pay-sum.html',context)
    
    
def pdf_generator(request,pk):
    account = Accounts.objects.get(user = request.user)
    payment = Payment.objects.get(ref_no= pk)
    reservation = Reservation.objects.get(user_id = request.user.id)
    service = Services.objects.get(service_id = reservation.service.service_id)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)
    
    list = []
    c.saveState()
    c.scale(1,-1)
    x_val = 0
    y_val = -800
    c.drawImage(ImageReader('static/images/Reservice.png'), x_val, y_val, width=600, height=800)
    c.restoreState()
   
    list.append(" ")
    list.append(" ")
    list.append(" ")
    list.append(" ")
    list.append(" ")
    list.append(" ")
    list.append(" ")
    list.append(" ")
    list.append(f"ReServation ID: {reservation.reservation_id}")
    list.append(" ")
    list.append(f"Account No: {account.acct_no}")
    list.append(" ")
    list.append(f"Client Name: {request.user.first_name} {request.user.last_name}")
    list.append(" ")
    list.append(f"Payment for: School Service")
    list.append(" ")
    list.append(f"Service: {service}")
    list.append(" ")
    list.append(f"Franchise: {service.franchise.franchise_name}")
    list.append(" ")
    list.append(f"Reservation Date: {reservation.created}")
    list.append(" ")
    list.append(f"Total: {payment.total} pesos")
    list.append(" ")
    
    
    
    
    
    
    for line in list:
        textob.textLine(line)
        
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf, as_attachment=True, filename='payment.pdf')
    
    
def otc_payments(request,pk):
    context={}
    return render(request,'main/otc_payment.html',context)

def bayad_center(request,pk):
    pass

def imc_tellering(request,pk):
    
    payment = Payment.objects.get(ref_no = pk)
    reservation = Reservation.objects.get(payment = payment)
    form = Proof_of_payment(instance = payment )
    
    if request.method == "POST":
        form = Proof_of_payment(request.POST,request.FILES,instance = payment )
        if form.is_valid():
            
            form.save()
            payment.status = "PENDING"
            payment.save()
            messages.success(request, 'Proof of payment successfully submitted')
            return redirect('stdnt-payment', pk = payment.ref_no)
    context={'reservation':reservation,'payment':payment,'form':form}
    return render(request,'main/imc_tellering.html',context)

def franchise_registration(request):
    form = FranchiseRegistrationForm()
    if request.method == 'POST':
        form = FranchiseRegistrationForm(request.POST,request.FILES)
        if form.is_valid() :
            form.save()

            messages.success(request,'We Received your request, please allow 3-5 business days for the approval of your request.')
            return redirect('identify')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    context = {'form':form}
    return render(request,'main/franchise/franchise-register.html', context)

def franchise_nav(request):
    franchise = Franchise.objects.get(user = request.user)
    context = {'franchise':franchise}
    return render(request,'main/franchise/franchise_nav.html',context)


def frannchise_drivers(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    franchise = Franchise.objects.get(user = request.user)
    
    franchiseDrivers = FranchiseDrivers.objects.filter(
        Q(driver_last_name__icontains = q)|
        Q(driver_first_name__icontains = q)|
        Q(driver_middle_name__icontains = q)|
        Q(status__icontains = q)|
        Q(email__icontains =q )
        
        ,franchise = franchise)
    context={'franchiseDrivers':franchiseDrivers, 'franchise':franchise}
    return render(request,'main/franchise/franchise-drivers.html',context)

def franchise_drivers_indiv(request,pk):

    fdriver= FranchiseDrivers.objects.get(driver_code = pk)
    
    context = {'fdriver':fdriver}
    
    return render(request,'main/franchise/franchise-drivers-individual.html',context)

def franchise_regiter_driver(request):
    form = FranchiseDriversForm()
    franchise = Franchise.objects.get(user = request.user)
    vehicles = Vehicle.objects.filter(franchise=franchise)
    
    #if not vehicles:
    #    return redirect('no-driver')
  
    if request.method == "POST":
        form = FranchiseDriversForm(request.POST,request.FILES)
        if form.is_valid():
            franchise_d = form.save(commit=False)
            franchise_d.franchise = franchise
            franchise_d.user=request.user
            franchise_d.save()
            current_date = datetime.datetime.now()  
            subject = 'ReService:Driver Registration'
            message = render_to_string("main/driver_registration_created_mssg.html", {
                                'operator':request.user,
                                'driver': franchise_d,
                                'date':current_date,
                            })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[request.user.email], fail_silently=False)
            messages.success(request,'request successfully submitted')
                
            return redirect('franchise-drivers')
    
    context = {'form':form}
    return render(request,'main/franchise/franchise_add_driver.html',context)

def no_drivers(request):
    return render(request,'main/franchise/no_driver.html')

def franchise_vehicles(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    franchise = Franchise.objects.get(user_id = request.user.id)
    vehicles = VehicleRequest.objects.filter(
        Q(model__icontains = q)|
        Q(plate_no__icontains = q)|
        Q(status__icontains = q)
        
        ,franchise=franchise,active=True)
    context ={'vehicles':vehicles,'franchise':franchise}
    return render(request,'main/franchise/franchise-vehicles.html',context)
    
def franchise_vehicles_individual_edit(request,pk):
    vehicle = VehicleRequest.objects.get(vehicle_id = pk)
    form = VehicleUpdateForm( instance=vehicle)
    
    if request.method == "POST":
        form = VehicleUpdateForm(request.POST,request.FILES, instance=vehicle)
        if form.is_valid():
            form.save(commit = False)
            vehicle.status = "PENDING"
            vehicle.save()
            current_date = datetime.datetime.now()  
            subject = 'ReService: Vehicle Infromation Update'
            message = render_to_string("main/vehilcle_edit_mssg.html", {
                                'operator':request.user,
                                'vehicle': vehicle,
                                'date':current_date,
                            })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[request.user.email], fail_silently=False)
            messages.success(request,'request successfully submitted')
            
            return redirect('franchise-vehicles')
    context ={'vehicle':vehicle, 'form':form}
    return render(request,'main/franchise/franchise-vehicles-indiv-edit.html',context)

def franchise_vehicles_retire(request,pk):
    pass 

def franchise_vehicles_individual(request,pk):
    vehicle = VehicleRequest.objects.get(vehicle_id = pk)
    context ={'vehicle':vehicle}
    return render(request,'main/franchise/franchise-vehicles-indiv.html',context)

def franchise_regisater_vehicle(request):
    form = VehicleForm()
    franchise = Franchise.objects.get(user = request.user)
 
     
    if request.method == "POST":
        form = VehicleForm(request.POST,request.FILES)
        
        if form.is_valid():
            vehicle = form.save(commit = False)
            vehicle.franchise = franchise
            vehicle.save()
            current_date = datetime.datetime.now()  
            subject = 'ReService:Vehicle Registration'
            message = render_to_string("main/vehicle_registation_mssg.html", {
                                'operator':franchise.user,
                                'vehicle': vehicle,
                                'date':current_date,
                            })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[request.user.email], fail_silently=False)
            messages.success(request, 'request submittted')
            return redirect('franchise-vehicles')

    context = {'form':form}
    return render(request,'main/franchise/franchise-vehicles-register.html',context)

def franchise_services(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    franchise = Franchise.objects.get(user = request.user)
    services = Services.objects.filter(
        Q(price__icontains = q)|
        Q(driver__user__last_name__icontains = q)|
        Q(driver__user__first_name__icontains = q)|
        Q(driver__user__middle_name__icontains = q)|
        Q(pick_up__icontains = q)|
        Q(franchise__franchise_name__icontains = q)|
        Q(status__icontains = q)
        ,franchise = franchise )
    context = {'services':services,'franchise':franchise}
    return render(request,'main/franchise/franchise-services.html',context)

def franchise_service_edit(request,pk):
    service = Services.objects.get(service_id = pk)
    form = ServicesForm(instance=service)
    
    if request.method == "POST":
        form = ServicesForm(request.POST,instance=service)
        if form.is_valid():
            serv= form.save(commit=False)
            serv.status = "PENDING"
            serv.save()
            current_date = datetime.datetime.now()  
            subject = 'ReService:Service Change'
            message = render_to_string("main/service_change_mssg.html", {
                                'service':service,
                                'date':current_date,
                            })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from,[request.user.email], fail_silently=False)
            messages.success(request, 'request submittted')
            return redirect('franchise-services')
            
    context = {'form':form,'service':service}
    return render(request,'main/franchise/franchise-service-edit.html',context)
    
def franchise_services_indiv(request,pk):
    page = "service"
    service = Services.objects.get(service_id = pk)
    
    context = {'service':service,'page':page}
    return render(request,'main/franchise/franchise-services-individual.html',context)

def franchise_services_register(request):
    form = ServiceRegister()
    
    franchise = Franchise.objects.get(user = request.user)
    drivers = Driverprofile.objects.filter( franchise = franchise)
    if request.method == "POST":
        form = ServiceRegister(request.POST)
        if form.is_valid():
            driver = request.POST.get('drivers')
            if driver is None:
                driver_user = None
            else:
                driver_user = Driverprofile.objects.get(user=driver )
            
            service = form.save(commit=False)
            service.franchise = franchise
            service.driver = driver_user
            service.save()
            messages.success(request,'request has been submitted')
            return redirect('franchise-services')
    context = {'form':form,'drivers':drivers}
    return render(request,'main/franchise/franchise-services-register.html',context)

def franchise_profile(request,pk):
    user = User.objects.get(id = pk)
    franchise = Franchise.objects.get(user = user)
    mydrivers = Driverprofile.objects.filter(franchise=franchise)
    vehicles = Vehicle.objects.filter(franchise = franchise)
    service = Services.objects.filter(franchise=franchise)
    payments = Payment.objects.filter(status = "SUCCESSFULL")
    total_list=[]
    payment_list = []
    for p in payments:
        if franchise == p.reservation.service.franchise:
           payment_list.append(p)
    
    user_list = []
    #get list of payments associated wuth the franchise
    for x in payment_list:
        payment = Payment.objects.get(ref_no = str(x))
        if payment.reservation.service.franchise == franchise:
            total_list.append(payment.total)
            user_list.append(payment.user.id)
    #get the user of payments in the user_list
    final_list = []   
    for y in user_list:
        user = User.objects.get( id = str(y))
        final_list.append(f"{user.first_name} {user.middle_name} {user.last_name}")
    
    #loop through the payment_list to get total
    total = 0
    for price in total_list:
        total = total + int(price)
    
    
    context={'user':user,'franchise':franchise,'mydrivers':mydrivers,'service':service,'vehicles':vehicles,"final_list":final_list, 'payment_list':payment_list,'total':total}
    return render(request,'main/franchise/franchise_profile.html',context)


def faq(request):
    return render(request,'main/faq.html')

def privacypolicy(request):
    return render(request,'main/privacynpolicies.html')

def termsncond(request):
    return render(request,'main/terms.html')