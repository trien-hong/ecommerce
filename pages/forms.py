from django import forms
from django.core.validators import validate_integer
from django.contrib.auth import get_user_model
from .choices import Choices # to see or edit the choices go to choices.py
User = get_user_model()

class Login(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter your username", "class": "field"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "class": "field"}))

    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) == 0:
            raise forms.ValidationError("Username length is 0 or is empty.")

        if len(username) > 30:
            raise forms.ValidationError("Username length is greater than 30.")

        return username

class Signup(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter your username", "class": "field"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "class": "field"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password", "class": "field"}))
    state_territory = forms.ChoiceField(label="State/territory (optional)", choices=Choices.CHOICES_STATE_TERRITORY, widget=forms.Select(attrs={"title": "You can always change this in your settings"}), required=False) # to see or edit the choices go to choices.py

    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) == 0:
            raise forms.ValidationError("Username length is 0 or is empty.")

        if len(username) > 30:
            raise forms.ValidationError("Username length is greater than 30.")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exist. Please try using a different username.")

        return username

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please ensure you are using the same password for both fields.")

        return confirm_password

    def clean_state_territory(self):
        state_territoy = self.cleaned_data["state_territory"]

        if len([i[0] for i in Choices.CHOICES_STATE_TERRITORY if i[0] == state_territoy]) == 0:
            raise forms.ValidationError("State/territory choice is not valid.")

        return state_territoy

class RestPassword(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter your username", "class": "field"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your new password", "class": "field"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm your new password", "class": "field"}))

    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) == 0:
            raise forms.ValidationError("Username length is 0 or is empty.")

        if len(username) > 30:
            raise forms.ValidationError("Username length is greater than 30.")

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
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter your new username", "class": "field"}))

    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) == 0:
            raise forms.ValidationError("Username length is 0 or is empty.")

        if len(username) > 30:
            raise forms.ValidationError("Username length is greater than 30.")

        if User.objects.filter(username=username).exists() == True:
            raise forms.ValidationError("Username already exist. Please try using a different username.")

        return username

class ChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your new password", "class": "field"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm your new password", "class": "field"}))

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please ensure you are using the same password for both fields.")

        return confirm_password

class UploadProfilePicture(forms.Form):
    picture = forms.ImageField(widget=forms.FileInput(attrs={"class": "field"}))

    def clean_picture(self):
        picture = self.cleaned_data["picture"]

        if picture.size > 5*1024*1024:
            raise forms.ValidationError("Image is greater than 5MB. Please upload an image that is less than 5MB.")

        return picture

class UploadBannerPicture(forms.Form):
    picture = forms.ImageField(widget=forms.FileInput(attrs={"class": "field"}))

    def clean_picture(self):
        picture = self.cleaned_data["picture"]

        if picture.size > 5*1024*1024:
            raise forms.ValidationError("Image is greater than 5MB. Please upload an image that is less than 5MB.")

        return picture

class ChangeStateTerritory(forms.Form):
    state_territory = forms.ChoiceField(label="State/territory (optional & 1st option to remove)", choices=Choices.CHOICES_STATE_TERRITORY, widget=forms.Select(attrs={"title": "You can always change this in your settings", "class": "field"}), required=False) # to see or edit the choices go to choices.py

    def clean_state_territory(self):
        state_territoy = self.cleaned_data["state_territory"]

        if len([i[0] for i in Choices.CHOICES_STATE_TERRITORY if i[0] == state_territoy]) == 0:
            raise forms.ValidationError("State/territory choice is not valid.")

        return state_territoy

class DeleteAccount(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your password to delete account", "class": "field"}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]

        if self.user.check_password(password) == False:
            raise forms.ValidationError("Password is incorrect. Please enter the correct password.")

        return password

class AddProduct(forms.Form):
    title = forms.CharField(max_length=50, label="Title *", widget=forms.TextInput(attrs={"placeholder": "Enter the product's title", "class": "field"}))
    picture = forms.ImageField(label="Picture *")
    description = forms.CharField(max_length=500, label="Description *", widget=forms.Textarea(attrs={"placeholder": "Enter the product's description", "rows": "5", "class": "field"}))
    category = forms.ChoiceField(label="Category *", choices=Choices.CHOICES_CATEGORY) # to see or edit the choices go to choices.py
    condition = forms.ChoiceField(label="Condition *", choices=Choices.CHOICES_CONDITION) # to see or edit the choices go to choices.py
    price = forms.DecimalField(label="Price (in $/USD) *", widget=forms.TextInput(attrs={"placeholder": "Enter the product's price (ie. 5.00, 10.50, 9,999.99, etc.)", "class": "field"}))
    upc = forms.CharField(min_length=12, max_length=12, label="UPC (optional)", widget=forms.TextInput(attrs={"placeholder": "Enter the product's Universal Product Code (UPC)", "class": "field"}), required=False)
    ean = forms.CharField(min_length=13, max_length=13, label="EAN (optional)", widget=forms.TextInput(attrs={"placeholder": "Enter the product's International Article Number (EAN)", "class": "field"}), required=False)

    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title) == 0:
            raise forms.ValidationError("Title length is 0 or is empty.")

        if len(title) > 50:
            raise forms.ValidationError("Title length is greater than 50.")

        return title

    def clean_picture(self):
        picture = self.cleaned_data["picture"]

        if picture.size > 5*1024*1024:
            raise forms.ValidationError("Image is greater than 5MB. Please upload an image that is less than 5MB.")

        return picture

    def clean_description(self):
        description = self.cleaned_data["description"]

        if len(description) == 0:
            raise forms.ValidationError("Description length is 0 or is empty.")

        if len(description) > 500:
            raise forms.ValidationError("Description length is greater than 500.")

        return description

    def clean_category(self):
        category = self.cleaned_data["category"]

        if category == "" or (category, category) not in Choices.CHOICES_CATEGORY: # to see or edit the choices go to choices.py
            raise forms.ValidationError("Category choice is not valid.")

        return category

    def clean_condition(self):
        condition = self.cleaned_data["condition"]

        if condition == "" or (condition, condition) not in Choices.CHOICES_CONDITION: # to see or edit the choices go to choices.py
            raise forms.ValidationError("Condition choice is not valid.")

        return condition

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price > 9999.99:
            raise forms.ValidationError("The max price is set at $9,999.99. Please lower the price.")

        return price

    def clean_upc(self):
        upc = self.cleaned_data["upc"]

        if upc != "":
            validate_integer(upc)

            if len(upc) < 12:
                raise forms.ValidationError("The UPC length is less than 12.")

            if len(upc) > 30:
                raise forms.ValidationError("The UPC length is greater than 12.")

            upc_list = [int(i) for i in upc]
            check_digit = upc_list[len(upc_list) - 1]
            total = 0
            odd_total = 0
            even_total = 0
            for i in range(len(upc_list) - 1):
                if i % 2 == 0:
                    even_total = even_total + upc_list[i]
                elif i % 2 != 0:
                    odd_total = odd_total + upc_list[i]
            total = even_total * 3 + odd_total + check_digit

            if total % 10 != 0:
                raise forms.ValidationError("The UPC you entered doesn't seem to be a valid UPC.")

        return upc

    def clean_ean(self):
        ean = self.cleaned_data["ean"]

        if ean != "":
            validate_integer(ean)

            if len(ean) < 13:
                raise forms.ValidationError("The EAN length is less than 13")

            if len(ean) > 13:
                raise forms.ValidationError("The EAN length is greater than 13")

            ean_list = [int(i) for i in ean]
            check_digit = ean_list[len(ean_list) - 1]
            total = 0
            odd_total = 0
            even_total = 0
            for i in range(len(ean_list) - 1):
                if i % 2 == 0:
                    even_total = even_total + ean_list[i]
                elif i % 2 != 0:
                    odd_total = odd_total + ean_list[i]
            total = even_total + odd_total * 3 + check_digit

            if total % 10 != 0:
                raise forms.ValidationError("The EAN you entered doesn't seem to be a valid EAN.")

        return ean

class EditProduct(forms.Form):
    CHOICES_PRODUCT_STATUS = [
        Choices.CHOICES_PRODUCT_STATUS[0],
        Choices.CHOICES_PRODUCT_STATUS[1],
        Choices.CHOICES_PRODUCT_STATUS[2]
    ] # to see or edit the choices go to choices.py

    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter the product's new title", "title": "Only edit a field if you need to", "class": "field"}), required=False)
    picture = forms.ImageField(widget=forms.FileInput(attrs={"title": "Only edit a field if you need to"}), required=False)
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"placeholder": "Enter the product's new description", "title": "Only edit a field if you need to", "rows": "6", "class": "field"}), required=False)
    category = forms.ChoiceField(choices=Choices.CHOICES_CATEGORY, widget=forms.Select(attrs={"title": "Only edit a field if you need to"}), required=False) # to see or edit the choices go to choices.py
    condition = forms.ChoiceField(choices=Choices.CHOICES_CONDITION, widget=forms.Select(attrs={"title": "Only edit a field if you need to"}), required=False) # to see or edit the choices go to choices.py
    upc = forms.CharField(min_length=12, max_length=12, label="UPC", widget=forms.TextInput(attrs={"placeholder": "Enter the product's Universal Product Code (UPC)", "title": "Only edit a field if you need to", "class": "field"}), required=False)
    ean = forms.CharField(min_length=13, max_length=13, label="EAN", widget=forms.TextInput(attrs={"placeholder": "Enter the product's International Article Number (EAN)", "title": "Only edit a field if you need to", "class": "field"}), required=False)
    status = forms.ChoiceField(choices=CHOICES_PRODUCT_STATUS, widget=forms.Select(attrs={"title": "Only edit a field if you need to"}), required=False) # to see or edit the choices go to choices.py

    def clean_title(self):
        title = self.cleaned_data["title"]

        if title != "":
            if len(title) > 50:
                raise forms.ValidationError("Title length is greater than 50.")

        return title

    def clean_picture(self):
        picture = self.cleaned_data["picture"]

        if picture is not None:
            if picture.size > 5*1024*1024:
                raise forms.ValidationError("Image is greater than 5MB. Please upload an image that is less than 5MB.")

        return picture

    def clean_description(self):
        description = self.cleaned_data["description"]

        if description != "":
            if len(description) > 500:
                raise forms.ValidationError("Description length is greater than 500.")

        return description

    def clean_category(self):
        category = self.cleaned_data["category"]

        if category != "":
            if (category, category) not in Choices.CHOICES_CATEGORY: # to see or edit the choices go to choices.py
                raise forms.ValidationError("Category choice is not valid.")

        return category

    def clean_condition(self):
        condition = self.cleaned_data["condition"]

        if condition != "":
            if (condition, condition) not in Choices.CHOICES_CONDITION: # to see or edit the choices go to choices.py
                raise forms.ValidationError("Condition choice is not valid.")

        return condition

    def clean_upc(self):
        upc = self.cleaned_data["upc"]

        if upc != "":
            validate_integer(upc)

            if len(upc) < 12:
                raise forms.ValidationError("The UPC length is less than 12.")

            if len(upc) > 12:
                raise forms.ValidationError("The UPC length is greater than 12.")

            upc_list = [int(i) for i in upc]
            check_digit = upc_list[len(upc_list) - 1]
            total = 0
            odd_total = 0
            even_total = 0
            for i in range(len(upc_list) - 1):
                if i % 2 == 0:
                    even_total = even_total + upc_list[i]
                elif i % 2 != 0:
                    odd_total = odd_total + upc_list[i]
            total = even_total * 3 + odd_total + check_digit

            if total % 10 != 0:
                raise forms.ValidationError("The UPC you entered doesn't seem to be a valid UPC.")

        return upc

    def clean_ean(self):
        ean = self.cleaned_data["ean"]

        if ean != "":
            validate_integer(ean)

            if len(ean) < 13:
                raise forms.ValidationError("The EAN length is less than 12.")

            if len(ean) > 13:
                raise forms.ValidationError("The EAN length is greater than 12.")

            ean_list = [int(i) for i in ean]
            check_digit = ean_list[len(ean_list) - 1]
            total = 0
            odd_total = 0
            even_total = 0
            for i in range(len(ean_list) - 1):
                if i % 2 == 0:
                    even_total = even_total + ean_list[i]
                elif i % 2 != 0:
                    odd_total = odd_total + ean_list[i]
            total = even_total + odd_total * 3 + check_digit

            if total % 10 != 0:
                raise forms.ValidationError("The EAN you entered doesn't seem to be a valid EAN.")

        return ean

    def clean_status(self):
        status = self.cleaned_data["status"]

        if status != "":
            if (status, status) not in Choices.CHOICES_PRODUCT_STATUS: # to see or edit the choices go to choices.py
                raise forms.ValidationError("Condition choice is not valid.")

        return status

class SearchProduct(forms.Form):
    title = forms.CharField(max_length=50, label="", widget=forms.TextInput(attrs={"class": "form-control me-2", "id": "product_search", "type": "search", "label": "", "placeholder": "Search...", "title": "Search for specific products (by title)", "size": "35"}), required=False)

    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title) == 0:
            raise forms.ValidationError("Title length is 0 or is empty.")

        if len(title) > 50:
            raise forms.ValidationError("Title length is greater than 50.")

        return title

class AdvancedSearchProduct(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter the product's title", "title": "Enter the product's title", "class": "field"}), required=False)
    category = forms.ChoiceField(choices=Choices.CHOICES_CATEGORY, widget=forms.Select(attrs={"title": "Choose the product's category"}), required=False) # to see or edit the choices go to choices.py
    condition = forms.ChoiceField(choices=Choices.CHOICES_CONDITION, widget=forms.Select(attrs={"title": "Choose the product's condition"}), required=False) # to see or edit the choices go to choices.py
    upc = forms.CharField(min_length=12, max_length=12, label="UPC", widget=forms.TextInput(attrs={"placeholder": "Enter the product's Universal Product Code (UPC)", "title": "Enter the product's Universal Product Code (UPC)", "class": "field"}), required=False)
    ean = forms.CharField(min_length=13, max_length=13, label="EAN", widget=forms.TextInput(attrs={"placeholder": "Enter the product's International Article Number (EAN)", "title": "Enter the product's International Article Number (EAN)", "class": "field"}), required=False)
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Enter the seller's username", "title": "Enter the seller's username", "class": "field"}), required=False)

    def clean_title(self):
        title = self.cleaned_data["title"]

        if title != "":
            if len(title) > 50:
                raise forms.ValidationError("Title length is greater than 50.")

        return title

    def clean_category(self):
        category = self.cleaned_data["category"]

        if category != "":
            if (category, category) not in Choices.CHOICES_CATEGORY: # to see or edit the choices go to choices.py
                raise forms.ValidationError("Category choice is not valid.")

        return category

    def clean_condition(self):
        condition = self.cleaned_data["condition"]

        if condition != "":
            if (condition, condition) not in Choices.CHOICES_CONDITION: # to see or edit the choices go to choices.py
                raise forms.ValidationError("Condition choice is not valid.")

        return condition

    def clean_upc(self):
        upc = self.cleaned_data["upc"]

        if upc != "":
            validate_integer(upc)

            if len(upc) < 12:
                raise forms.ValidationError("The UPC length is less than 12.")

            if len(upc) > 12:
                raise forms.ValidationError("The UPC length is greater than 12.")

            upc_list = [int(i) for i in upc]
            check_digit = upc_list[len(upc_list) - 1]
            total = 0
            odd_total = 0
            even_total = 0
            for i in range(len(upc_list) - 1):
                if i % 2 == 0:
                    even_total = even_total + upc_list[i]
                elif i % 2 != 0:
                    odd_total = odd_total + upc_list[i]
            total = even_total * 3 + odd_total + check_digit

            if total % 10 != 0:
                raise forms.ValidationError("The UPC you entered doesn't seem to be a valid UPC.")

        return upc

    def clean_ean(self):
        ean = self.cleaned_data["ean"]

        if ean != "":
            validate_integer(ean)

            if len(ean) < 13:
                raise forms.ValidationError("The EAN length is less than 12.")

            if len(ean) > 13:
                raise forms.ValidationError("The EAN length is greater than 12.")

            ean_list = [int(i) for i in ean]
            check_digit = ean_list[len(ean_list) - 1]
            total = 0
            odd_total = 0
            even_total = 0
            for i in range(len(ean_list) - 1):
                if i % 2 == 0:
                    even_total = even_total + ean_list[i]
                elif i % 2 != 0:
                    odd_total = odd_total + ean_list[i]
            total = even_total + odd_total * 3 + check_digit

            if total % 10 != 0:
                raise forms.ValidationError("The EAN you entered doesn't seem to be a valid EAN.")

        return ean

    def clean_username(self):
        username = self.cleaned_data["username"]

        if username != "":
            if len(username) > 30:
                raise forms.ValidationError("Username length is greater than 30.")

        return username

class UpcEanLookup(forms.Form):
    upc = forms.CharField(min_length=12, max_length=12, label="UPC", widget=forms.TextInput(attrs={"placeholder": "Enter the product's Universal Product Code (UPC)", "title": "Enter the product's Universal Product Code (UPC)", "class": "field"}), required=False)
    ean = forms.CharField(min_length=13, max_length=13, label="EAN", widget=forms.TextInput(attrs={"placeholder": "Enter the product's International Article Number (EAN)", "title": "Enter the product's International Article Number (EAN)", "class": "field"}), required=False)

    def clean_upc(self):
        upc = self.cleaned_data["upc"]

        if upc != "":
            validate_integer(upc)

            if len(upc) < 12:
                raise forms.ValidationError("The UPC length is less than 12.")

            if len(upc) > 12:
                raise forms.ValidationError("The UPC length is greater than 12.")

            upc_list = [int(i) for i in upc]
            check_digit = upc_list[len(upc_list) - 1]
            total = 0
            odd_total = 0
            even_total = 0
            for i in range(len(upc_list) - 1):
                if i % 2 == 0:
                    even_total = even_total + upc_list[i]
                elif i % 2 != 0:
                    odd_total = odd_total + upc_list[i]
            total = even_total * 3 + odd_total + check_digit

            if total % 10 != 0:
                raise forms.ValidationError("The UPC you entered doesn't seem to be a valid UPC.")

        return upc

    def clean_ean(self):
        ean = self.cleaned_data["ean"]

        if ean != "":
            validate_integer(ean)

            if len(ean) < 13:
                raise forms.ValidationError("The EAN length is less than 12.")

            if len(ean) > 13:
                raise forms.ValidationError("The EAN length is greater than 12.")

            ean_list = [int(i) for i in ean]
            check_digit = ean_list[len(ean_list) - 1]
            total = 0
            odd_total = 0
            even_total = 0
            for i in range(len(ean_list) - 1):
                if i % 2 == 0:
                    even_total = even_total + ean_list[i]
                elif i % 2 != 0:
                    odd_total = odd_total + ean_list[i]
            total = even_total + odd_total * 3 + check_digit

            if total % 10 != 0:
                raise forms.ValidationError("The EAN you entered doesn't seem to be a valid EAN.")

        return ean

class Feedback(forms.Form):
    overall_rating = forms.ChoiceField(choices=Choices.CHOICES_OVERALL_RATING, widget=forms.Select(attrs={"title": "Choose the overall rating", "class": "field"})) # to see or edit the choices go to choices.py
    accurate_description = forms.ChoiceField(choices=Choices.CHOICES_FEEDBACK_RATING, widget=forms.Select(attrs={"placeholder": "How accurate was the product's description", "title": "How accurate was the product's description", "class": "field"}))
    shipping_speed = forms.ChoiceField(choices=Choices.CHOICES_FEEDBACK_RATING, widget=forms.Select(attrs={"placeholder": "How reasonable was the shipping speed", "title": "How reasonable was the shipping speed", "class": "field"}))
    shipping_cost = forms.ChoiceField(choices=Choices.CHOICES_FEEDBACK_RATING, widget=forms.Select(attrs={"placeholder": "How reasonable was the shipping cost", "title": "How reasonable was the shipping cost", "class": "field"}))
    communication = forms.ChoiceField(choices=Choices.CHOICES_FEEDBACK_RATING, widget=forms.Select(attrs={"placeholder": "How was the seller's communication", "title": "How was the seller's communication", "class": "field"}))
    comment = forms.CharField(max_length=250, widget=forms.Textarea(attrs={"placeholder": "A simple sentence or two that described your experience", "title": "A simple sentence or two that described your experience", "rows": "4", "class": "field"}))

    def clean_overall_rating(self):
        overall_rating = self.cleaned_data["overall_rating"]

        if len([i[0] for i in Choices.CHOICES_OVERALL_RATING if i[0] == overall_rating]) == 0:
            raise forms.ValidationError("Overall rating is not valid.")

        return overall_rating

    def clean_accurate_description(self):
        accurate_description = int(self.cleaned_data["accurate_description"])

        if len([i[0] for i in Choices.CHOICES_FEEDBACK_RATING if i[0] == accurate_description]) == 0:
            raise forms.ValidationError("Accurate description rating is not valid. Must be 1-5.")

        return accurate_description

    def clean_shipping_speed(self):
        shipping_speed = int(self.cleaned_data["shipping_speed"])

        if len([i[0] for i in Choices.CHOICES_FEEDBACK_RATING if i[0] == shipping_speed]) == 0:
            raise forms.ValidationError("Shipping speed rating is not valid. Must be 1-5.")

        return shipping_speed

    def clean_shipping_cost(self):
        shipping_cost = int(self.cleaned_data["shipping_cost"])

        if len([i[0] for i in Choices.CHOICES_FEEDBACK_RATING if i[0] == shipping_cost]) == 0:
            raise forms.ValidationError("Shipping cost rating is not valid. Must be 1-5.")

        return shipping_cost

    def clean_communication(self):
        communication = int(self.cleaned_data["communication"])

        if len([i[0] for i in Choices.CHOICES_FEEDBACK_RATING if i[0] == communication]) == 0:
            raise forms.ValidationError("Communication rating is not valid. Must be 1-5.")

        return communication

    def clean_comment(self):
        comment = self.cleaned_data["comment"]

        if len(comment) == 0:
            raise forms.ValidationError("The comment length is 0 or is empty.")

        if len(comment) > 250:
            raise forms.ValidationError("The comment length is greater than 250.")

        return comment
