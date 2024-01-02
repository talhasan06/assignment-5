from .constants import GENDER_TYPE
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserAccount,UserAddress

class UserRegistrationForm(UserCreationForm):
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length = 100)

    class Meta:
        model = User
        fields=['username','password1','password2','first_name','last_name','email','birth_date','gender','postal_code','city','country','street_address']

    def save(self,commit=True):
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
            print(f'User saved with ID: {our_user.id}')

            gender=self.cleaned_data.get('gender')
            postal_code=self.cleaned_data.get('postal_code')
            country=self.cleaned_data.get('country')
            birth_date=self.cleaned_data.get('birth_date')
            city=self.cleaned_data.get('city')
            street_address=self.cleaned_data.get('street_address')

            try:
                UserAddress.objects.create(
                    user=our_user,
                    postal_code=postal_code,
                    country=country,
                    city=city,
                    street_address=street_address,
                )

                UserAccount.objects.create(
                    user=our_user,
                    gender=gender,
                    birth_date=birth_date,
                    account_no=100000 + our_user.id
                )

                print('UserAddress and UserAccount created successfully')
            except Exception as e:
                print(f'Error creating UserAddress and UserAccount: {e}')
                
        return our_user
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200'
                    'text-gray-700 border border-gray-200 rounded'
                    'py-3 px-4 leading-light focus:outline-none'
                    'focus:bg-white focus:border-gray-500'
                )
            })

class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        # jodi user er account thake 
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserAccount.objects.get_or_create(user=user) 
            user_address, created = UserAddress.objects.get_or_create(user=user) 

            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
    