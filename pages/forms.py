from django import forms
# from django.core.files.images import get_image_dimensions
from django.contrib.auth import get_user_model
User = get_user_model()

class Login(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'size': '25'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'size': '25'}))

class Signup(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'size': '25'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'size': '25'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'size': '25'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exist. Please try using a different username.')
        return username
    
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match. Please ensure you are using the same password for both fields.')
        return confirm_password

class RestPassword(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'size': '25'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'size': '25'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'size':  '25'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists() == False:
            raise forms.ValidationError('Username does not exist. Please try using a different username.')
        return username
    
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match. Please ensure you are using the same password for both fields.')
        return confirm_password

class AddProduct(forms.Form):
    # i'll add in more categories and possible more fields later
    CHOICES_CATEGORY = [
        ("kitchen", "kitchen"),
        ("living room", "living room"),
        ("garage", "garage"),
        ("bathroom", "bathroom"),
        ("bedroom", "bedroom"),
        ("office", "office"),
        ("outdoor", "outdoor"),
        ("toys", "toys"),
        ("games", "games"),
        ("clothing", "clothing"),
        ("electronics", "electronics"),
        ("mechanical parts", "mechanical parts")
    ]

    title = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Enter the product title', 'size': '30'}))
    picture = forms.ImageField()
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"rows": "6"}))
    category = forms.TypedChoiceField(choices=CHOICES_CATEGORY)

    # i can't seem to validate the picture within the form. i'll try again later.
    # def clean_picture(self):
        # picture = self.cleaned_data['picture']
        # w, h = get_image_dimensions(picture)
        # if picture.size > 5*1024*1024:
        #     raise forms.ValidationError('Image is greater than 5MB. Please upload an image that is less than 5MB.')
        # return picture