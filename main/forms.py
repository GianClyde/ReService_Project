from django import forms 
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm,PasswordResetForm
from django.forms import ModelForm
from .models import Reservation,User,Profile,Driverprofile,StudentUser,DriverUser,Vehicle,ReservationCancelation,Announcement,Franchise
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple
# Create your forms here.

from django import forms
User = get_user_model()


# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(), 
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance
class DriverUserForm(UserCreationForm):
    class Meta:
        model = DriverUser
        fields = ('email','password1','password2','first_name','last_name','middle_name','contact_no')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'text',
            'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password1',
            'id':'password1',
            'type':'text',
            'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password2',
            'id':'password2',
            'type':'text',
            'placeholder':'Re enter Password'})
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'first_name',
            'id':'first_name',
            'type':'text',
            'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'last_name',
            'id':'last_name',
            'type':'text',
            'placeholder':'Last Name'})
        self.fields['middle_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'middle_name',
            'id':'middle_name',
            'type':'text',
            'placeholder':'Middle Name'})
        self.fields['contact_no'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'contact_no',
            'id':'contact_no',
            'type':'text',
            'placeholder':'contact_no'})


class NotAdminDriverUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','middle_name','contact_no')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'first_name',
            'id':'first_name',
            'type':'text',
            'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'last_name',
            'id':'last_name',
            'type':'text',
            'placeholder':'Last Name'})
        self.fields['middle_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'middle_name',
            'id':'middle_name',
            'type':'text',
            'placeholder':'Middle Name'})
        self.fields['contact_no'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'contact_no',
            'id':'contact_no',
            'type':'text',
            'placeholder':'contact_no'})

 
class StudentUserForm(UserCreationForm):
    class Meta:
        model = StudentUser
        fields = ('email','password1','password2','first_name','last_name','middle_name','contact_no')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'text',
            'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password1',
            'id':'password1',
            'type':'text',
            'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password2',
            'id':'password2',
            'type':'text',
            'placeholder':'Re enter Password'})
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'first_name',
            'id':'first_name',
            'type':'text',
            'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'last_name',
            'id':'last_name',
            'type':'text',
            'placeholder':'Last Name'})
        self.fields['middle_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'middle_name',
            'id':'middle_name',
            'type':'text',
            'placeholder':'Middle Name'})
        self.fields['contact_no'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'contact_no',
            'id':'contact_no',
            'type':'text',
            'placeholder':'contact_no'})

class ProfilePicture(ModelForm):
    image = forms.ImageField(label="Profile Pciture")
    class Meta:
        model = Profile
        fields=('image',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'form-input'})

class DriverProfilePicture(ModelForm):
    image = forms.ImageField(label="Profile Pciture")
    class Meta:
        model = Driverprofile
        fields=('image',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'form-input'})
class CancelationForm(ModelForm):
   class Meta:
        model=ReservationCancelation
        fields = ('reason',)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['reason'].widget.attrs.update({
                'class': 'form-input',
                'required':'',
                'name':'reason',
                'id':'reason',
                'type':'text',
                'placeholder':'Cancelation reason'})
        
class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields= ('parent','parent_contactNo','parent_address','birth_date','lot','street','village','city','zipcode',
                 'age','school_branch','section','year_level')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'parent',
            'id':'parent',
            'type':'text',
            'placeholder':'parent'})
        self.fields['parent_contactNo'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'parent_contactNo',
            'id':'parent_contactNo',
            'type':'text',
            'placeholder':'parent contact number'})
        self.fields['parent_address'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'parent_address',
            'id':'parent_address',
            'type':'text',
            'placeholder':'parent address'})
        self.fields['birth_date'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'birth_date',
            'id':'birth_date',
            'type': 'date',
            'placeholder': 'yyyy-mm-dd (DOB)'})
        self.fields['lot'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'lot',
            'id':'lot',
            'type':'text',
            'placeholder':'lot/house no,/bldg no.'})
        self.fields['street'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'street',
            'id':'street',
            'type':'text',
            'placeholder':'street'})
        self.fields['village'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'village',
            'id':'village',
            'type':'text',
            'placeholder':'village'})
        self.fields['city'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'city',
            'id':'city',
            'type':'text',
            'placeholder':'city'})
        self.fields['zipcode'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'zipcode',
            'id':'zipcode',
            'type':'text',
            'placeholder':'zipcode'})
        self.fields['age'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'age',
            'id':'age',
            'type':'text',
            'placeholder':'age'})
        self.fields['school_branch'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'school_branch',
            'id':'school_branch',
            'placeholder':'school_branch'})
        self.fields['section'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'section',
            'id':'section',
            'type':'text',
            'placeholder':'section'})
        self.fields['year_level'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'year_level',
            'id':'year_level',
            'type':'text',
            'placeholder':'year level'})
        


class AdminEditDriverProfileForm(ModelForm):
    class Meta:
        model=Driverprofile
        fields= ('birth_date','lot','street','village','city','zipcode',
                 'age',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'birth_date',
            'id':'birth_date',
            'type': 'date',
            'placeholder': 'yyyy-mm-dd (DOB)'})
        self.fields['lot'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'lot',
            'id':'lot',
            'type':'text',
            'placeholder':'lot/house no,/bldg no.'})
        self.fields['street'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'street',
            'id':'street',
            'type':'text',
            'placeholder':'street'})
        self.fields['village'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'village',
            'id':'village',
            'type':'text',
            'placeholder':'village'})
        self.fields['city'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'city',
            'id':'city',
            'type':'text',
            'placeholder':'city'})
        self.fields['zipcode'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'zipcode',
            'id':'zipcode',
            'type':'text',
            'placeholder':'zipcode'})
        self.fields['age'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'age',
            'id':'age',
            'type':'text',
            'placeholder':'age'})
        
class EditProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields= ('parent','parent_contactNo','parent_address','birth_date','lot','street','village','city','zipcode',
                 'age')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'parent',
            'id':'parent',
            'type':'text',
            'placeholder':'parent'})
        self.fields['parent_contactNo'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'parent_contactNo',
            'id':'parent_contactNo',
            'type':'text',
            'placeholder':'parent contact number'})
        self.fields['parent_address'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'parent_address',
            'id':'parent_address',
            'type':'text',
            'placeholder':'parent address'})
        self.fields['birth_date'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'birth_date',
            'id':'birth_date',
            'type': 'date',
            'placeholder': 'yyyy-mm-dd (DOB)'})
        self.fields['lot'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'lot',
            'id':'lot',
            'type':'text',
            'placeholder':'lot/house no,/bldg no.'})
        self.fields['street'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'street',
            'id':'street',
            'type':'text',
            'placeholder':'street'})
        self.fields['village'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'village',
            'id':'village',
            'type':'text',
            'placeholder':'village'})
        self.fields['city'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'city',
            'id':'city',
            'type':'text',
            'placeholder':'city'})
        self.fields['zipcode'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'zipcode',
            'id':'zipcode',
            'type':'text',
            'placeholder':'zipcode'})
        self.fields['age'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'age',
            'id':'age',
            'type':'text',
            'placeholder':'age'})

        
class DriverProfileForm(ModelForm):
    class Meta:
        model=Driverprofile
        fields= ('image','birth_date','lot','street','village','city','zipcode',
                 'age','school_branch','assigned_route','vehicle','franchise')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['franchise'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'franchise',
            'id':'franchise',
            'type': 'franchise',
            'placeholder': 'Franchise'})
        self.fields['vehicle'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'vehicle',
            'id':'vehicle',
            'type':'text',
            'placeholder':'Vehicle'})

        self.fields['assigned_route'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'assigned_route',
            'id':'assigned_route',
            'type':'text',
            'placeholder':'Route'})

        self.fields['birth_date'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'birth_date',
            'id':'birth_date',
            'type': 'date',
            'placeholder': 'yyyy-mm-dd (DOB)'})
        self.fields['lot'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'lot',
            'id':'lot',
            'type':'text',
            'placeholder':'lot/house no,/bldg no.'})
        self.fields['street'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'street',
            'id':'street',
            'type':'text',
            'placeholder':'street'})
        self.fields['village'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'village',
            'id':'village',
            'type':'text',
            'placeholder':'village'})
        self.fields['city'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'city',
            'id':'city',
            'type':'text',
            'placeholder':'city'})
        self.fields['zipcode'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'zipcode',
            'id':'zipcode',
            'type':'text',
            'placeholder':'zipcode'})
        self.fields['age'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'age',
            'id':'age',
            'type':'text',
            'placeholder':'age'})
        self.fields['school_branch'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'school_branch',
            'id':'school_branch',
            'placeholder':'school_branch'})
    

class NotAdminDriverProfileForm(ModelForm):
    class Meta:
        model=Driverprofile
        fields= ('image','birth_date','lot','street','village','city','zipcode',
                 'age',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['birth_date'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'birth_date',
            'id':'birth_date',
            'type': 'date',
            'placeholder': 'yyyy-mm-dd (DOB)'})
        self.fields['lot'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'lot',
            'id':'lot',
            'type':'text',
            'placeholder':'lot/house no,/bldg no.'})
        self.fields['street'].widget.attrs.update({
            'class': 'form-input-add',
            'required':'',
            'name':'street',
            'id':'street',
            'type':'text',
            'placeholder':'street'})
        self.fields['village'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'village',
            'id':'village',
            'type':'text',
            'placeholder':'village'})
        self.fields['city'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'city',
            'id':'city',
            'type':'text',
            'placeholder':'city'})
        self.fields['zipcode'].widget.attrs.update({
            'class': 'form-input-add2',
            'required':'',
            'name':'zipcode',
            'id':'zipcode',
            'type':'text',
            'placeholder':'zipcode'})
        self.fields['age'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'age',
            'id':'age',
            'type':'text',
            'placeholder':'age'})

    
class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','middle_name','contact_no')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'first_name',
            'id':'first_name',
            'type':'text',
            'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'last_name',
            'id':'last_name',
            'type':'text',
            'placeholder':'Last Name'})
        self.fields['middle_name'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'middle_name',
            'id':'middle_name',
            'type':'text',
            'placeholder':'Middle Name'})
        self.fields['contact_no'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'contact_no',
            'id':'contact_no',
            'type':'text',
            'placeholder':'contact_no'})

    
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['new_password1'].widget.attrs.update({
                'class': 'form-input',
                'required':'',
                'name':'new_password1',
                'id':'new_password1',
                'type':'text',
                'placeholder':'new password'})
            self.fields['new_password2'].widget.attrs.update({
                'class': 'form-input',
                'required':'',
                'name':'new_password2',
                'id':'new_password2',
                'type':'text',
                'placeholder':'re-enter new password'})

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
                'class': 'form-input',
                'required':'',
                'name':'email',
                'id':'email',
                'type':'text',
                'placeholder':'Email'})
        
class ReservationEditForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ('user','driver','reservation_status','payment_status',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'user',
            'id':'user',
            'type':'text',
            'placeholder':'user'})
        self.fields['driver'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'user',
            'id':'user',
            'type':'text',
            'placeholder':'user'})
        self.fields['reservation_status'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'reservation_status',
            'id':'reservation_status',
            'type':'text',
            'placeholder':'reservation_status'})
        self.fields['payment_status'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'payment_status',
            'id':'payment_status',
            'type':'text',
            'placeholder':'payment_status'})
    
class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ('model','image','plate_no','capacity','included')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'model',
            'id':'model',
            'type':'text',
            'placeholder':'model'})
        self.fields['image'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'image',
            'id':'image',
            'type':'text',
            'placeholder':'image'})
        self.fields['plate_no'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'plate_no',
            'id':'plate_no',
            'type':'text',
            'placeholder':'plate_no'})
        self.fields['capacity'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'capacity',
            'id':'capacity',
            'type':'text',
            'placeholder':'capacity'})
        self.fields['included'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'included',
            'id':'included',
            'type':'text',
            'placeholder':'included'})
        
class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ('title','content',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'title',
            'id':'title',
            'type':'text',
            'placeholder':'title'})
        self.fields['content'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'content',
            'id':'content',
            'type':'text',
            'placeholder':'content'})
        
class FranchiseForm(ModelForm):
    class Meta:
        model = Franchise
        fields = ('franchise_name','franchise_no','operator')
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['franchise_name'].widget.attrs.update({
                'class': 'form-input',
                'required':'',
                'name':'franchise_name',
                'id':'franchise_name',
                'type':'text',
                'placeholder':'franchise_name'})
            self.fields['franchise_no'].widget.attrs.update({
                'class': 'form-input1',
                'required':'',
                'name':'franchise_no',
                'id':'franchise_no',
                'type':'text',
                'placeholder':'franchise_no'})
            self.fields['operator'].widget.attrs.update({
                'class': 'form-input1',
                'required':'',
                'name':'operator',
                'id':'operator',
                'type':'text',
                'placeholder':'operator'})