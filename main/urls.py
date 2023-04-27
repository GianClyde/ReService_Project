from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [
    path('', views.identify, name='identify'),


    path('login/', views.login_page, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/',views.registerUser,name='register'),
    path('profile-fillup/',views.profile_fillUp,name='profile-fillup'),
    path('reservation',views.reservation,name='reservation'),
    path('reservation-driver-info/<str:pk>/',views.reservation_driver_info,name='driver-info-reservation'),
    path('reservation-process/<str:pk>/',views.reserve_service,name='reserve-service'),

    path('waiting-cancelation/',views.waiting_cancelation,name="wait-cancel"),
    path('reserved_not_confirmed/', views.existing_reservation, name='cancel-reserve'),
    path('driver-reservation-decline/<str:pk>/',views.driver_reservation_declined,name="drvr-decline-rsrv"),
    path('driver-reservation-accept/<str:pk>/',views.driver_reservation_accpeted,name="drvr-accept-rsrv"),
    path('driver-reservations', views.driver_reservations, name="driver-reservations"),
    path('driver-reservations-info/<str:pk>/',views.driver_reservation_info, name="driver-reserve-info"),
    path('driver-login/', views.driver_login_page, name='driver-login'),
    path('driver-register/', views.driver_register_page, name='driver-register'),
    path('driver-mainNavbPage/',views.drivermainNavPage,name='DrivernavPage'),
    path('driver-profile-fillup/',views.driver_profile_fillUp,name='driver-profile-fillup'),
    path('driver-profile/<str:pk>/', views.driver_profile_page, name='driver-profile'),
    path('driver-security-settings/<str:pk>/', views.driver_security_settings, name='driver-security'),
    path('driver-edit-profile/<str:pk>/', views.edit_driver_profile, name='driver-edit-profile'),

    path('change_password', views.password_change, name='change-password'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('registration-identify',views.registration_choices,name="registration-choose"),
    
    path('mainNavbPage/',views.mainNavPage,name='navPage'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('edit-profile/<str:pk>/', views.editProfile, name='edit-profile'),
    path('main-reservation-page/', views.main_reservation, name='main-reservation'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('not-allowed/', views.not_allowed, name='not-allowed'),
     path('announcement/', views.announcements, name='announcement'),
     
    path('admin-nav/', views.admin_nav_page, name="admin-nav"),
    path('admin-students/', views.admin_students,name="admin-students"),
    path('admin-student/delete/<str:pk>/' ,views.admin_student_delete,name="stdnt-dlt"),
    path('admin-indiv-students/<str:pk>/', views.admin_students_indiv, name="admin-stdnt-info"),
    path('admin-stdnt-edit/<str:pk>/', views.admin_student_edit, name="admin-stdnt-edit"),
    path('admin-drivers/', views.admin_drivers,name="admin-drivers"),
    path('admin-indiv-drivers/<str:pk>/', views.admin_drivers_indiv, name="admin-drvr-info"),
    path('admin-drvr-edit/<str:pk>/',views.admin_driver_edit,name="admin-drvr-edit"),
    path('admin-reservations/', views.admin_reservations,name="admin-reservations"),
    path('admin-indiv-reservations/<str:pk>/', views.admin_reservation_indiv, name="admin-rsrv-info"),
    path('admin-reservations-edit/<str:pk>/', views.admin_reservation_edit, name="admin-rsrvtns-edit"),
    path('admin-reservations-accept/<str:pk>/', views.admin_reservation_accept, name="admin-rsrvtns-accept"),
    path('admin-reservations-decline/<str:pk>/', views.admin_reservation_decline, name="admin-rsrvtns-decline"),
     path('admin-indiv-cancelations/<str:pk>/', views.admin_cancelation_individual, name="admin-cancelations-info"),
    path('admin-reservation-cancelations',views.admin_reservation_cancelations,name="reservation-cancelation"),
    path('admin-cancelation-accept/<str:pk>/', views.admin_cancelation_accept,name="accept-cancel"),
    path('admin-cancelation-decline/<str:pk>/',views.admin_cancelation_decline,name="admin-cancelation-decline"),
    path('admin-vehicles/',views.admin_vehicles,name='vehicles'),
    path('admin-vehicles-individual/<str:pk>/',views.admin_vehicles_individual,name='vehicles-individual'),
    path('admin-vehicle/delete/<str:pk>/' ,views.admin_vehicle_delete,name="vhcl-dlt"),
    path('admin-vhcl-edit/<str:pk>/',views.admin_vehicle_edit,name="vhcl-edit")
]
