from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class Login(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter your username", "size": "30"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "size": "30"}))

class Signup(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter your username", "size": "30"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "size": "30"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password", "size": "30"}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exist. Please try using a different username.")
        return username
    
    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please ensure you are using the same password for both fields.")
        return confirm_password

class RestPassword(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter your username", "size": "30"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "size": "30"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password", "size": "30"}))

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists() == False:
            raise forms.ValidationError("Username does not exist. Please try using a different username.")
        return username
    
    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please ensure you are using the same password for both fields.")
        return confirm_password
    
class ChangeUsername(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter your new username", "size": "35"}))
    
    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists() == True:
            raise forms.ValidationError("Username already exist. Please try using a different username.")
        return username

class ChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your new password", "size": "35"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm your new password", "size": "35"}))

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please ensure you are using the same password for both fields.")
        return confirm_password

class DeleteAccount(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your password to delete account", "size": "35"}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]

        if self.user.check_password(password) == False:
            raise forms.ValidationError("Password is incorrect. Please enter the correct password.")
        return password

class AddProduct(forms.Form):
    # i'll add in more categories and possible more fields later

    PLEASE_CHOOSE_CATEGORY = ""
    KITCHEN = "kitchen"
    LIVING_ROOM = "living room"
    GARAGE = "garage"
    BATHROOM = "bathroom"
    BEDROOM = "bedroom"
    OFFICE = "office"
    OUTDOOR = "outdoor"
    TOYS = "toys"
    GAMES = "games"
    CLOTHING = "clothing"
    ELECTRONICS = "electronics"

    CHOICES_CATEGORY = [
        (PLEASE_CHOOSE_CATEGORY, "Choose a category"),
        (KITCHEN, "kitchen"),
        (LIVING_ROOM, "living room"),
        (GARAGE, "garage"),
        (BATHROOM, "bathroom"),
        (BEDROOM, "bedroom"),
        (OFFICE, "office"),
        (OUTDOOR, "outdoor"),
        (TOYS, "toys"),
        (GAMES, "games"),
        (CLOTHING, "clothing"),
        (ELECTRONICS, "electronics")
    ]

    PLEASE_CHOOSE_CONDITION = ""
    NEW = "new"
    OPEN_BOX = "open box"
    PREOWNED = "preowned"
    USED_LIKE_NEW = "use (like new)"
    USED_MODERATELY = "used (moderately)"
    USED_HEAVILY = "used (heavily)"
    BROKEN_UNUSABLE = "broken (unusable)"

    CHOICES_CONDITION = [
        (PLEASE_CHOOSE_CONDITION, "Choose a condition"),
        (NEW, "new"),
        (OPEN_BOX, "open box"),
        (PREOWNED, "preowned"),
        (USED_LIKE_NEW, "used (like new)"),
        (USED_MODERATELY, "used (moderately)"),
        (USED_HEAVILY, "used (heavily)"),
        (BROKEN_UNUSABLE, "broken (unusable)")
    ]

    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter the product's title", "size": "35"}))
    picture = forms.ImageField()
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"placeholder": "Enter the product's description", "rows": "6"}))
    category = forms.ChoiceField(choices=CHOICES_CATEGORY)
    condition = forms.ChoiceField(choices=CHOICES_CONDITION)

    def clean_picture(self):
        picture = self.cleaned_data["picture"]
        
        if picture.size > 5*1024*1024:
            raise forms.ValidationError("Image is greater than 5MB. Please upload an image that is less than 5MB.")
        return picture
    
class EditProduct(forms.Form):
    # i'll add in more categories and possible more fields later

    PLEASE_CHOOSE_CATEGORY = ""
    KITCHEN = "kitchen"
    LIVING_ROOM = "living room"
    GARAGE = "garage"
    BATHROOM = "bathroom"
    BEDROOM = "bedroom"
    OFFICE = "office"
    OUTDOOR = "outdoor"
    TOYS = "toys"
    GAMES = "games"
    CLOTHING = "clothing"
    ELECTRONICS = "electronics"

    CHOICES_CATEGORY = [
        (PLEASE_CHOOSE_CATEGORY, "Choose a new category"),
        (KITCHEN, "kitchen"),
        (LIVING_ROOM, "living room"),
        (GARAGE, "garage"),
        (BATHROOM, "bathroom"),
        (BEDROOM, "bedroom"),
        (OFFICE, "office"),
        (OUTDOOR, "outdoor"),
        (TOYS, "toys"),
        (GAMES, "games"),
        (CLOTHING, "clothing"),
        (ELECTRONICS, "electronics")
    ]

    PLEASE_CHOOSE_CONDITION = ""
    NEW = "new"
    OPEN_BOX = "open box"
    PREOWNED = "preowned"
    USED_LIKE_NEW = "use (like new)"
    USED_MODERATELY = "used (moderately)"
    USED_HEAVILY = "used (heavily)"
    BROKEN_UNUSABLE = "broken (unusable)"

    CHOICES_CONDITION = [
        (PLEASE_CHOOSE_CONDITION, "Choose a new condition"),
        (NEW, "new"),
        (OPEN_BOX, "open box"),
        (PREOWNED, "preowned"),
        (USED_LIKE_NEW, "used (like new)"),
        (USED_MODERATELY, "used (moderately)"),
        (USED_HEAVILY, "used (heavily)"),
        (BROKEN_UNUSABLE, "broken (unusable)")
    ]

    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter the product's new title", "size": "35", "title": "Only edit what you need to"}), required=False)
    picture = forms.ImageField(widget=forms.FileInput(attrs={"title": "Only edit what you need to"}), required=False)
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"placeholder": "Enter the product's new description", "rows": "6", "title": "Only edit what you need to"}), required=False)
    category = forms.ChoiceField(choices=CHOICES_CATEGORY, widget=forms.Select(attrs={"title": "Only edit what you need to"}), required=False)
    condition = forms.ChoiceField(choices=CHOICES_CONDITION, widget=forms.Select(attrs={"title": "Only edit what you need to"}), required=False)

    def clean_picture(self):
        picture = self.cleaned_data["picture"]
        
        if picture is not None:
            if picture.size > 5*1024*1024:
                raise forms.ValidationError("Image is greater than 5MB. Please upload an image that is less than 5MB.")
        return picture