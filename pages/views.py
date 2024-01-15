import os
import uuid
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from . import forms
from . models import Product
from . models import Cart
from . models import Sold
User = get_user_model()

@never_cache
def login_view(request):
    """
    URL: /login/
    """
    if request.method == "GET":
        login_form = forms.Login()
        return render(request, "login.html", { "login_form": login_form })
    if request.method == "POST":
        user_info = request.POST
        login_form = forms.Login(user_info)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data["username"], password=login_form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect(index_view)
            else:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>The username and/or password seem to be incorrect. Please try agian.</li></ul>"))
                return redirect(login_view)
        else:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>The username and/or password seem to be incorrect. Please try agian.</li></ul>"))
            return redirect(login_view)

@never_cache
def signup_view(request):
    """
    URL: /signup/
    """
    if request.method == "GET":
        signup_form = forms.Signup()
        return render(request, "signup.html", { "signup_form": signup_form })
    if request.method == "POST":
        user_info = request.POST
        signup_form = forms.Signup(user_info)
        if signup_form.is_valid():
            user = User.objects.create_user(username=signup_form.cleaned_data["username"], password=signup_form.cleaned_data["password"])
            messages.add_message(request, messages.SUCCESS, "User has been successfully created. You may now login.")
            return redirect(signup_view)
        else:
            error_string = get_form_errors(signup_form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(signup_view)

@never_cache
def reset_password_view(request):
    """
    URL: /reset-password/
    """
    if request.method == "GET":
        # i hope to one day add verfication to this
        reset_password_form = forms.RestPassword()
        return render(request, "reset_password.html", { "reset_password_form": reset_password_form})
    if request.method == "POST":
        user_info = request.POST
        reset_password_form = forms.RestPassword(user_info)
        if reset_password_form.is_valid():
            user = User.objects.get(username=reset_password_form.cleaned_data["username"])
            user.set_password(reset_password_form.cleaned_data["confirm_password"])
            user.save()
            messages.add_message(request, messages.SUCCESS, "The password associated with the username has been reset. You may now login.")
            return redirect(reset_password_view)
        else:
            error_string = get_form_errors(reset_password_form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(reset_password_view)

@never_cache
@login_required
def index_view(request):
    """
    URL: /index/ OR /
    """
    if request.method == "GET":
        user = request.user
        products = Product.objects.all().exclude(bought=True)
        return render(request, "index.html", { "current_username": user.username, "products": products })

@never_cache
@login_required
def product_view(request, id):
    """
    URL: /product/id/<int:id>/
    Where <int:id> is the id of the product being viewed
    """
    if request.method == "GET":
        try:
            user = request.user
            product = Product.objects.get(id=id)
            if product.seller != user:
                product.views = product.views + 1
                product.save()
        except Product.DoesNotExist:
            product = None
        return render(request, "product.html", { "current_username": user.username, "product": product })

@never_cache
@login_required
def add_product_view(request):
    """
    URL: /product/add-product/
    """
    if request.method == "GET":
        add_product_form = forms.AddProduct()
        return render(request, "add_product.html", { "add_product_form": add_product_form })
    if request.method == "POST":
        user = request.user
        product_info = request.POST
        picture = request.FILES
        add_product_form = forms.AddProduct(product_info, picture)
        if add_product_form.is_valid():
            file_extension = add_product_form.cleaned_data["picture"].name.split(".")[-1]
            add_product_form.cleaned_data["picture"].name = "product_picture_id_" + str(uuid.uuid4()) + "." + file_extension
            product = Product(title=product_info["title"], picture=add_product_form.cleaned_data["picture"], description=product_info["description"], category=product_info["category"], condition=product_info["condition"], seller=user, bought=False, views=0)
            product.save()
            messages.add_message(request, messages.SUCCESS, "Your product, \"" + product.title + "\" has been successfully added. Image less than/greater than 500x500 have been upsized/downsized and cropped to the middle and center.")
            return redirect(add_product_view)
        else:
            error_string = get_form_errors(add_product_form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(add_product_view)

@never_cache
@login_required
def delete_product_view(request, id):
    """
    URL: /product/delete-product/id/<int:id>/
    where <int:id> is the id of the product that you want to delete
    """
    if request.method == "GET":
        return redirect(profile_option_view, option="listing-history")
    if request.method == "POST":
        user = request.user
        try:
            product = Product.objects.get(id=id)
            if product.seller != user or product.bought == True:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in deleting this product from your profile. Please try again.</li></ul>"))
                return redirect(profile_option_view, option="listing-history")
            else:
                product.delete()
                messages.add_message(request, messages.SUCCESS, "You successfully deleted the product, \"" + product.title + "\", from your profile.")
                return redirect(profile_option_view, option="listing-history")
        except Product.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in deleting this product from your profile. Please try again.</li></ul>"))
            return redirect(profile_option_view, option="listing-history")

@never_cache
@login_required
def edit_product_view(request, id):
    """
    URL: /product/edit-product/id/<int:id>/
    where <int:id> is the id of the product that you want to edit
    """
    if request.method == "GET":
        user = request.user
        edit_product_form = forms.EditProduct()
        try:
            product = Product.objects.get(id=id)
            if product.seller != user or product.bought == True:
                product = None
        except Product.DoesNotExist:
            product = None
        return render(request, "edit_product.html", { "product": product, "edit_product_form": edit_product_form })
    if request.method == "POST":
        product_info = request.POST
        picture = request.FILES
        edit_product_form = forms.EditProduct(product_info, picture)
        if edit_product_form.is_valid():
            try:
                product = Product.objects.get(id=id)
                if edit_product_form.cleaned_data["title"] == "" and edit_product_form.cleaned_data["picture"] is None and edit_product_form.cleaned_data["description"] == "" and edit_product_form.cleaned_data["category"] == "" and edit_product_form.cleaned_data["condition"] == "":
                    messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Seems like you submitted an empty form.</li><li>If you have nothing to edit on the product, please don't edit it.</li></ul>"))
                    return redirect(edit_product_view, id)
                else:
                    if edit_product_form.cleaned_data["title"] != "":
                        product.title = edit_product_form.cleaned_data["title"]
                    if edit_product_form.cleaned_data["picture"] is not None:
                        if os.path.exists(product.picture.path):
                            os.remove(product.picture.path)
                        file_extension = edit_product_form.cleaned_data["picture"].name.split(".")[-1]
                        edit_product_form.cleaned_data["picture"].name = "product_picture_id_" + str(uuid.uuid4()) + "." + file_extension
                        product.picture = edit_product_form.cleaned_data["picture"]
                    if edit_product_form.cleaned_data["description"] != "":
                        product.description = edit_product_form.cleaned_data["description"]
                    if edit_product_form.cleaned_data["category"] != "":
                        product.category = edit_product_form.cleaned_data["category"]
                    if edit_product_form.cleaned_data["condition"] != "":
                        product.condition = edit_product_form.cleaned_data["condition"]
                    product.save()
                    messages.add_message(request, messages.SUCCESS, "Your product have been successfully updated.")
                    return redirect(edit_product_view, id)
            except Product.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in editing your product. Please try again.</li></ul>"))
                return redirect(edit_product_view, id)
        else:
            error_string = get_form_errors(edit_product_form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(edit_product_view, id)

@never_cache
@login_required
def cart_view(request):
    """
    URL: /cart/
    """
    if request.method == "GET":
        user = request.user
        cart = Cart.objects.filter(user=user)
        return render(request, "cart.html", { "cart": cart })

@never_cache
@login_required
def add_to_cart_view(request, id):
    """
    URL: /cart/add-to-cart/id/<int:id>/
    where <int:id> is the id of product being added to cart
    """
    if request.method == "GET":
        return redirect(product_view, id=id)
    if request.method == "POST":
        try:
            user = request.user
            product = Product.objects.get(id=id)
            if product.bought == True:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Sorry, this product, \"" + product.title + "\" is now sold out.</li></ul>"))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            elif product.seller == user:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>You cannot add your own product to the cart.</li></ul>"))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            elif Cart.objects.filter(product=product, user=user).exists():
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>This product, \"" + product.title + "\" already exist in your cart.</li></ul>"))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            else:
                cart = Cart(product=product, user=user)
                cart.save()
                messages.add_message(request, messages.SUCCESS, "You've successfully added, \"" + product.title + "\", to your cart.")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Product.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in adding this product to your cart.</li></ul>"))
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@never_cache
@login_required
def delete_from_cart_view(request, id):
    """
    URL: /cart/delete-from-cart/id/<int:id>/
    where <int:id> is the id of the item being removed from the cart
    """
    if request.method == "GET":
        return redirect(cart_view)
    if request.method == "POST":
        try:
            item = Cart.objects.get(id=id)
            item.delete()
            messages.add_message(request, messages.SUCCESS, "The product, \"" + item.product.title + "\", has been successfully removed from your cart.")
            return redirect(cart_view)
        except Cart.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in removing this product from your cart.</li></ul>"))
            return redirect(cart_view)

@never_cache
@login_required
def delete_all_items_from_cart_view(request):
    """
    URL: /cart/delete-all-items-from-cart/
    """
    if request.method == "GET":
        return redirect(cart_view)
    if request.method == "POST":
        user = request.user
        cart = Cart.objects.filter(user=user)
        cart.delete()
        messages.add_message(request, messages.SUCCESS, "All products within your cart has been removed. Your cart is now empty.")
        return redirect(cart_view)

@never_cache
@login_required
def check_out_view(request):
    """
    URL: /cart/check-out/
    """
    if request.method == "GET":
        return redirect(cart_view)
    if request.method == "POST":
        already_bought = 0
        user = request.user
        cart = Cart.objects.filter(user=user)
        for item in cart:
            try:
                product = Product.objects.get(id=item.product.id)
                if product.bought == False:
                    product.bought = True
                    product.save()
                    sold = Sold(product=product, buyer=user)
                    sold.save()
                    item.delete()
                else:
                    already_bought = already_bought + 1
            except Product.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seemed to be an error with one, some, or all your items in your cart.</li><li>It's possible the seller delisted an item in your cart.</li></ul>"))
                return redirect(cart_view)
        if already_bought == 0:
            messages.add_message(request, messages.SUCCESS, "Checkout was successful. All the items in your cart have been bought by you.")
            return redirect(cart_view)
        elif already_bought == 1:
            if cart.count() == already_bought:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Checkout was unsuccessful. The item you wanted to buy has been bought by another person.</li></ul>"))
                return redirect(cart_view)
            else:
                messages.add_message(request, messages.SUCCESS, "Checkout was successful. However, there was 1 item that has been bought by another person and that item is now marked by \"SOLD OUT\". That 1 item will not be purchased.")
                return redirect(cart_view)
        else:
            if cart.count() == already_bought:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Checkout was unsuccessful. The item(s) you wanted to buy has been bought by another person.</li></ul>"))
                return redirect(cart_view)
            else:
                messages.add_message(request, messages.SUCCESS, "Checkout was successful. However, some item(s) has been bought by another person and those item(s) are now marked by \"SOLD OUT\". There was a total of " + str(already_bought) + " item(s) bought already. Those item(s) will not be purchased.")
                return redirect(cart_view)

@never_cache
@login_required
def profile_view(request):
    """
    URL: /profile/
    """
    if request.method == "GET":
        user = request.user
        return render(request, "profile.html", { "user": user, "option": None })

@never_cache
@login_required
def profile_option_view(request, option):
    """
    URL: /profile/<str:option>/
    where <str:option> is either "settings", "wish-list", "listing-history", "purchase-history", or "login-history" and if not simply redirect to profile page
    """
    if request.method == "GET":
        user = request.user
        if option == "settings":
            # i hope to one day add verfication to these
            change_username_form = forms.ChangeUsername()
            change_password_form = forms.ChangePassword()
            delete_account_form = forms.DeleteAccount()
            return render(request, "profile.html", { "user": user, "option": "settings", "change_username_form": change_username_form, "change_password_form": change_password_form, "delete_account_form": delete_account_form })
        elif option == "wish-list":
            return render(request, "profile.html", { "user": user, "option": "wish-list" })
        elif option == "listing-history":
            listing_history = Product.objects.filter(seller=user)
            return render(request, "profile.html", { "user": user, "option": "listing-history", "listing_history": listing_history })
        elif option == "purchase-history":
            purchase_history = Sold.objects.filter(buyer=user)
            return render(request, "profile.html", { "user": user, "option": "purchase-history", "purchase_history": purchase_history })
        elif option == "login-history":
            return render(request, "profile.html", { "user": user, "option": "login-history" })
        else:
            return redirect(profile_view)

@never_cache
@login_required
def change_username_view(request):
    """
    URL: /profile/settings/change-username/
    """
    if request.method == "GET":
        return redirect(profile_option_view, option="settings")
    if request.method == "POST":
        user_info = request.POST
        change_username_form = forms.ChangeUsername(user_info)
        if change_username_form.is_valid():
            try:
                user = User.objects.get(id=request.user.id)
                user.username = change_username_form.cleaned_data["username"]
                user.save()
                messages.add_message(request, messages.SUCCESS, "Your username is now \"" + change_username_form.cleaned_data["username"] +"\". Everything associated with the username has now been updated.")
                return redirect(profile_option_view, option="settings")
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seemed to be an error in updating your username. Please try again.</li></ul>"))
                return redirect(profile_option_view, option="settings")
        else:
            error_string = get_form_errors(change_username_form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(profile_option_view, option="settings")

@never_cache
@login_required
def change_password_view(request):
    """
    URL: /profile/settings/change-password/
    """
    if request.method == "GET":
        return redirect(profile_option_view, option="settings")
    if request.method == "POST":
        user_info = request.POST
        change_password_form = forms.ChangePassword(user_info)
        if change_password_form.is_valid():
            try:
                user = User.objects.get(id=request.user.id)
                user.set_password(change_password_form.cleaned_data["password"])
                user.save()
                messages.add_message(request, messages.SUCCESS, "Your password has been successfully updated. You must login again with the new password.")
                return redirect(profile_option_view, option="settings")
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seemed to be an error in updating your password. Please try again.</li></ul>"))
                return redirect(profile_option_view, option="settings")
        else:
            error_string = get_form_errors(change_password_form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(profile_option_view, option="settings")

@never_cache
@login_required
def delete_account_view(request):
    """
    URL: /profile/settings/delete-account/
    """
    if request.method == "GET":
        return redirect(profile_option_view, option="settings")
    if request.method == "POST":
        user_info = request.POST
        delete_account_form = forms.DeleteAccount(user_info, user=request.user)
        if delete_account_form.is_valid():
            try:
                user = User.objects.get(id=request.user.id)
                user.delete()
                messages.add_message(request, messages.SUCCESS, "Your account has been deleted. Thank you for using our service!")
                return redirect(login_view)
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seemed to be an error in deleting your account. Please try again.</li></ul>"))
                return redirect(profile_option_view, option="settings")
        else:
            error_string = get_form_errors(delete_account_form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(profile_option_view, option="settings")

@never_cache
@login_required
def confirm_message_view(request, type):
    """
    URL: /confirm-message/type/<str:type>/
    where <str:type> is any one of the following below
    """
    if request.method == "GET":
        if type == "check-out":
            messages.add_message(request, messages.WARNING, "Are you sure you want to proceed with check out?", extra_tags="check-out")
            return redirect(cart_view)
        elif type == "delete-all-items-from-cart":
            messages.add_message(request, messages.WARNING, "Are you sure you want to delete all items in your cart?", extra_tags="delete-all-items-from-cart")
            return redirect(cart_view)
        elif type == "delete-product":
            messages.add_message(request, messages.WARNING, "Are you sure you want to delete this product from your profile?", extra_tags="delete-product")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@never_cache
@login_required
def logout_user(request):
    """
    URL: /logout-user/
    """
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout successful!")
    return redirect(login_view)

def get_form_errors(form):
    errors = list(form.errors.values())
    error_string = "<ul>"
    for i in range(len(errors)):
        error_string = error_string + "<li>" + str(list(form.errors.values())[i][0]) + "</li>"
    return error_string + "</ul>"