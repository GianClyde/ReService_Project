from django import forms 
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm,PasswordResetForm
from django.forms import ModelForm
from .models import Services,Schedule,DriverFeedback,DriverPayment,Vehicle,VehicleRequest,VehicleUpdateRequest,FranchiseDrivers,Reservation,User,Profile,Driverprofile,StudentUser,DriverUser,ReservationCancelation,Announcement,Franchise,Payment
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
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
        fields = ('email','first_name','last_name','middle_name','contact_no')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'text',
            'placeholder':'Email'})
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

class DriverFranchise(ModelForm):
    class Meta:
        model = Driverprofile
        fields=('franchise',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['franchise'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'franchise',
            'id':'franchise',
            'type':'text',
            'placeholder':' franchise'})

class DriverPaymentProof(ModelForm):
    class Meta:
        model = DriverPayment
        fields=('proof',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proof'].widget.attrs.update({
            'class': 'proof',
            'required':'',
            'name':'proof',
            'id':'proof',
            'type':'text',
            'placeholder':' proof'})
        
class FranchiseDriversForm(ModelForm):
    class Meta:
        model = FranchiseDrivers
        fields=('driver_last_name','driver_first_name','driver_middle_name','id_pic','nbi_clearance','liscense','email','contact_no','vehicle',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'vehicle',
            'id':'vehicle',
            'type':'text',
            'placeholder':' vehicle'})
        self.fields['contact_no'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'contact_no',
            'id':'contact_no',
            'type':'text',
            'placeholder':' contact_no'})
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'text',
            'placeholder':' email'})
        self.fields['driver_last_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'driver_last_name',
            'id':'driver_last_name',
            'type':'text',
            'placeholder':' driver_last_name'})
        self.fields['driver_first_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'driver_first_name',
            'id':'driver_first_name',
            'type':'text',
            'placeholder':' driver_first_name'})
        self.fields['driver_middle_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'driver_middle_name',
            'id':'driver_middle_name',
            'type':'text',
            'placeholder':' driver_middle_name'})
        
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

class AdmineditStudent(ModelForm):
    class Meta:
        model = StudentUser
        fields = ('email','first_name','last_name','middle_name','contact_no')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'text',
            'placeholder':'Email'})
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
                 'age','section','year_level')
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
                 'age','school_branch',)
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

class AdminFranchiseDriversDocs(ModelForm):
    class Meta:
        model = FranchiseDrivers
        fields = ('nbi_clearance','liscense',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nbi_clearance'].widget.attrs.update({
            'class': 'form-control',
            'required':'False',
            'name':'nbi_clearance',
            'id':'nbi_clearance',
            'type':'text',
            'placeholder':'nbi_clearance'})
        self.fields['liscense'].widget.attrs.update({
            'class': 'form-control',
            'required':'False',
            'name':'liscense',
            'id':'liscense',
            'type':'text',
            'placeholder':'liscense'})
        
        
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
        fields = ('franchise_name','franchise_no')
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
            
            
class Proof_of_payment(ModelForm):
    class Meta:
        model = Payment
        fields = ('proof',)
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['proof'].widget.attrs.update({
                    'class': 'form-input',
                    'required':'',
                    'name':'proof',
                    'id':'proof',
                    'type':'text',
                    'placeholder':'proof'})
        
class ReservationForm(ModelForm):
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
                    'name':'driver',
                    'id':'driver',
                    'type':'text',
                    'placeholder':'driver'})
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
                
class FranchiseDocs(ModelForm):
    class Meta:
        model = Franchise
        fields = ('franchise_doc','valid_id',)
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['franchise_doc'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'franchise_doc',
                    'id':'franchise_doc',
                    'type':'text',
                    'placeholder':'franchise_doc'})
                self.fields['valid_id'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'valid_id',
                    'id':'valid_id',
                    'type':'text',
                    'placeholder':'valid_id'})
class adminFranchiseRegistrationForm(ModelForm):
        class Meta:
            model = Franchise
            fields = ('franchise_name','franchise_no','valid_id','franchise_doc',)
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['franchise_name'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'franchise_name',
                    'id':'franchise_name',
                    'type':'text',
                    'placeholder':'franchise_name'})
                self.fields['franchise_no'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'franchise_no',
                    'id':'franchise_no',
                    'type':'text',
                    'placeholder':'service'})
               
class FranchiseRegistrationForm(ModelForm):
    class Meta:
        model = Franchise
        fields = ('franchise_name','franchise_no','operator_lastN','operator_middleN','operator_firstN','email','valid_id','franchise_doc','contact_no')
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['franchise_name'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'franchise_name',
                    'id':'franchise_name',
                    'type':'text',
                    'placeholder':'franchise_name'})
                self.fields['franchise_no'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'franchise_no',
                    'id':'franchise_no',
                    'type':'text',
                    'placeholder':'service'})
                self.fields['operator_lastN'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'operator_lastN',
                    'id':'operator_lastN',
                    'type':'text',
                    'placeholder':'operator_lastN'})
                self.fields['operator_middleN'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'operator_middleN',
                    'id':'operator_middleN',
                    'type':'text',
                    'placeholder':'operator_middleN'})
                self.fields['operator_firstN'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'operator_firstN',
                    'id':'operator_firstN',
                    'type':'text',
                    'placeholder':'operator_firstN'})
                self.fields['email'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'email',
                    'id':'email',
                    'type':'text',
                    'placeholder':'email'})
                self.fields['valid_id'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'valid_id',
                    'id':'valid_id',
                    'type':'text',
                    'placeholder':'valid_id'})
                self.fields['franchise_doc'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'franchise_doc',
                    'id':'franchise_doc',
                    'type':'text',
                    'placeholder':'franchise_doc'})
                self.fields['contact_no'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'contact_no',
                    'id':'contact_no',
                    'type':'text',
                    'placeholder':'contact_no'})
                

    
              
class VehicleUpdateForm(ModelForm):
      class Meta:
        model = VehicleRequest
        fields = ('model','image','plate_no','capacity','OR','CR',)
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['model'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'model',
                    'id':'model',
                    'type':'text',
                    'placeholder':'model'})
                self.fields['image'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'image',
                    'id':'image',
                    'type':'text',
                    'placeholder':'image'})
                self.fields['plate_no'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'plate_no',
                    'id':'plate_no',
                    'type':'text',
                    'placeholder':'plate_no'})
                self.fields['capacity'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'capacity',
                    'id':'capacity',
                    'type':'text',
                    'placeholder':'capacity'})
                self.fields['OR'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'OR',
                    'id':'OR',
                    'type':'text',
                    'placeholder':'OR'})
                self.fields['CR'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'CR',
                    'id':'CR',
                    'type':'text',
                    'placeholder':'CR'})
                
class VehicleForm(ModelForm):
    class Meta:
        model = VehicleRequest
        fields = ('model','image','plate_no','capacity','OR','CR',)


    def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['model'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'model',
                    'id':'model',
                    'type':'text',
                    'placeholder':'model'})
                self.fields['image'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'image',
                    'id':'image',
                    'type':'text',
                    'placeholder':'image'})
                self.fields['plate_no'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'plate_no',
                    'id':'plate_no',
                    'type':'text',
                    'placeholder':'plate_no'})
                self.fields['capacity'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'capacity',
                    'id':'capacity',
                    'type':'text',
                    'placeholder':'capacity'})
                self.fields['OR'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'OR',
                    'id':'OR',
                    'type':'text',
                    'placeholder':'OR'})
                self.fields['CR'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'CR',
                    'id':'CR',
                    'type':'text',
                    'placeholder':'CR'})
          
class AdminVehicleForm(ModelForm):
    class Meta:
        model = VehicleRequest
 
        fields = ('model','franchise','image','plate_no','capacity','OR','CR','status',)
    def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['status'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'status',
                    'id':'status',
                    'type':'text',
                    'placeholder':'status'})
                self.fields['franchise'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'franchise',
                    'id':'franchise',
                    'type':'text',
                    'placeholder':'franchise'})
                self.fields['model'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'model',
                    'id':'model',
                    'type':'text',
                    'placeholder':'model'})
                self.fields['image'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'image',
                    'id':'image',
                    'type':'text',
                    'placeholder':'image'})
                self.fields['plate_no'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'plate_no',
                    'id':'plate_no',
                    'type':'text',
                    'placeholder':'plate_no'})
                self.fields['capacity'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'capacity',
                    'id':'capacity',
                    'type':'text',
                    'placeholder':'capacity'})
                self.fields['OR'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'OR',
                    'id':'OR',
                    'type':'text',
                    'placeholder':'OR'})
                self.fields['CR'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'CR',
                    'id':'CR',
                    'type':'text',
                    'placeholder':'CR'})
class adminAddServices(ModelForm):
     class Meta:
        model = Services
        fields = ('price','driver','pick_up','franchise','status',)
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['price'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'price',
                    'id':'price',
                    'type':'text',
                    'placeholder':'price'})
                self.fields['driver'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'driver',
                    'id':'driver',
                    'type':'text',
                    'placeholder':'driver'})
                self.fields['pick_up'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'pick_up',
                    'id':'pick_up',
                    'type':'text',
                    'placeholder':'zipcode'})
                self.fields['franchise'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'franchise',
                    'id':'franchise',
                    'type':'text',
                    'placeholder':'franchise'})
                self.fields['status'].widget.attrs.update({
                    'class': 'form',
                    'required':'',
                    'name':'status',
                    'id':'status',
                    'type':'text',
                    'placeholder':'status'})


class ServiceRegister(ModelForm):
    class Meta:
        model = Services
        fields = ('price','pick_up',)
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['price'].widget.attrs.update({
                    'class': 'serv',
                    'required':'',
                    'name':'price',
                    'id':'price',
                    'type':'text',
                    'placeholder':'price'})
                self.fields['pick_up'].widget.attrs.update({
                    'class': 'serv',
                    'required':'',
                    'name':'pick_up',
                    'id':'pick_up',
                    'type':'text',
                    'placeholder':'pick_up'})

class ServicesForm(ModelForm):
    class Meta:
        model = Services
        fields = ('price','pick_up','driver',)
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['driver'].widget.attrs.update({
                    'class': 'serv',
                    'required':'',
                    'name':'driver',
                    'id':'driver',
                    'type':'text',
                    'placeholder':'driver'})
                self.fields['price'].widget.attrs.update({
                    'class': 'serv',
                    'required':'',
                    'name':'price',
                    'id':'price',
                    'type':'text',
                    'placeholder':'price'})
                self.fields['pick_up'].widget.attrs.update({
                    'class': 'serv',
                    'required':'',
                    'name':'pick_up',
                    'id':'pick_up',
                    'type':'text',
                    'placeholder':'pick_up'})


class PickUpTimeForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ('monday_pickUp','tuesday_pickUp','wednesday_pickUp','thursday_pickUp','friday_pickUp')
        widgets = {
                'monday_pickUp' : TimePickerInput(),
                'tuesday_pickUp' : TimePickerInput(),
                'wednesday_pickUp' : TimePickerInput(),
                'thursday_pickUp' : TimePickerInput(),
                'friday_pickUp' : TimePickerInput(),
                
            }
        
class ScheduleForm(ModelForm):
        class Meta:
            model = Schedule
            fields = ('monday_start','mondy_dismiss','tuesday_start','tuesday_dismiss','wednesday_start','wednesday_dismiss','thursday_start','thursday_dismiss','friday_start','friday_dismiss',)
        
            widgets = {
                'monday_start' : TimePickerInput(),
                'mondy_dismiss' : TimePickerInput(),
                'tuesday_start' : TimePickerInput(),
                'tuesday_dismiss' : TimePickerInput(),
                'wednesday_start' : TimePickerInput(),
                'wednesday_dismiss' : TimePickerInput(),
                'thursday_start' : TimePickerInput(),
                'thursday_dismiss' : TimePickerInput(),
                'friday_start' : TimePickerInput(),
                'friday_dismiss' : TimePickerInput(),
            }
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
          
                self.fields['monday_start'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'monday_start',
                    'id':'monday_start',
                    'type':'time',
                    'placeholder':'monday_start'})
                self.fields['mondy_dismiss'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'monday_dismiss',
                    'id':'monday_dismiss',
                    'type':'time',
                    'placeholder':'mondy_dismiss'})
                self.fields['tuesday_start'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'tuesday_start',
                    'id':'tuesday_start',
                    'type':'time',
                    'placeholder':'tuesday_start'})
                self.fields['tuesday_dismiss'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'tuesday_dismiss',
                    'id':'tuesday_dismiss',
                    'type':'time',
                    'placeholder':'tuesday_dismiss'})
                self.fields['wednesday_start'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'tuesday_start',
                    'id':'tuesday_start',
                    'type':'time',
                    'placeholder':'wednesday_start'})
                self.fields['wednesday_dismiss'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'wednesday_dismiss',
                    'id':'wednesday_dismiss',
                    'type':'time',
                    'placeholder':'wednesday_dismiss'})
                self.fields['thursday_start'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'thursday_start',
                    'id':'thursday_start',
                    'type':'time',
                    'placeholder':'thursday_start'})
                self.fields['thursday_dismiss'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'thursday_dismiss',
                    'id':'thursday_dismiss',
                    'type':'time',
                    'placeholder':'thursday_dismiss'})
                self.fields['friday_start'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'friday_start',
                    'id':'friday_start',
                    'type':'time',
                    'placeholder':'friday_start'})
                self.fields['friday_dismiss'].widget.attrs.update({
                    'class': 'sched',
                    'required':'',
                    'name':'friday_dismiss',
                    'id':'friday_dismiss',
                    'type':'time',
                    'placeholder':'friday_dismiss'})

NUMS= [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),

    ]


class CHOICES(forms.Form):
    NUMS = forms.CharField(widget=forms.RadioSelect(choices=NUMS))

    
class DriverFeedbackForm(ModelForm):
    class Meta:
        model = DriverFeedback
        fields = ('evaluation', 'concern')
    def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
          
                self.fields['evaluation'].widget.attrs.update({
                    'class': 'eval',
                    'required':'',
                    'name':'evaluation',
                    'id':'evaluation',
                    'type':'text',
                    'placeholder':'Enter Evaluation here'})
                self.fields['concern'].widget.attrs.update({
                    'class': 'eval',
                    'required':'',
                    'name':'concern',
                    'id':'concern',
                    'type':'text',
                    'placeholder':'Enter concern here'})
                

