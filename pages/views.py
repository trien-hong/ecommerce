import uuid
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from . models import Product
from . models import Cart
from . models import Sold
# Create your views here.

@never_cache
def login_view(request):
    if request.method == "GET":
        login_form = forms.Login()
        return render(request, 'login.html', { 'login_form': login_form })
    if request.method == "POST":
        user_info = request.POST
        form = forms.Login(user_info)
        if form.is_valid():
            user = authenticate(request, username=user_info["username"], password=user_info["password"])
            if user is not None:
                login(request, user)
                return redirect(index_view)
            else:
                messages.add_message(request, messages.ERROR, mark_safe("<li>The username and/or password seem to be incorrect. Please try agian.</li>"))
                return redirect(login_view)
        else:
            messages.add_message(request, messages.ERROR, mark_safe("<li>The username and/or password seem to be incorrect. Please try agian.</li>"))
            return redirect(login_view)

@never_cache
def signup_view(request):
    if request.method == "GET":
        signup_form = forms.Signup()
        return render(request, 'signup.html', { 'signup_form': signup_form })
    if request.method == "POST":
        user_info = request.POST
        form = forms.Signup(user_info)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            messages.add_message(request, messages.SUCCESS, "User has been successfully created. You may now login.")
            return redirect(signup_view)
        else:
            error_string = get_form_errors(form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(signup_view)

@never_cache
def reset_password_view(request):
    if request.method == "GET":
        reset_password_form = forms.RestPassword()
        return render(request, 'reset_password.html', { 'reset_password_form': reset_password_form})
    if request.method == "POST":
        user_info = request.POST
        form = forms.RestPassword(user_info)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data["username"])
            user.set_password(form.cleaned_data["confirm_password"])
            user.save()
            messages.add_message(request, messages.SUCCESS, "The password associated with the username has been reset. You may now login.")
            return redirect(reset_password_view)
        else:
            error_string = get_form_errors(form)
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(reset_password_view)

@never_cache
@login_required
def index_view(request):
    if request.method == "GET":
        products = Product.objects.all().exclude(bought=True)
        return render(request, 'index.html', { 'products': products })

@never_cache
@login_required
def product_view(request, id):
    if request.method == "GET":
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            product = None
        return render(request, 'product.html', { 'product': product })

@never_cache
@login_required
def add_product_view(request):
    if request.method == "GET":
        add_product_form = forms.AddProduct()
        return render(request, 'add_product.html', { 'add_product_form': add_product_form })
    if request.method == "POST":
        product_info = request.POST
        picture = request.FILES['picture']
        user = User.objects.get(id=request.user.id)
        # i can't seem to validate the picture within the form. i'll try again later.
        if picture.size > 5*1024*1024:
            messages.add_message(request, messages.ERROR, mark_safe("<li>Image is greater than 5MB. Please upload an image that is less than 5MB.</li>"))
            return redirect(add_product_view)
        else:
            ext = picture.name.split(".")[-1]
            picture.name = "product_picture_id_" + str(uuid.uuid4())[:13] + "." + ext
            product = Product(title=product_info['title'], picture=picture, description=product_info['description'], category=product_info['category'], lister=user, bought=False)
            product.save()
            messages.add_message(request, messages.SUCCESS, "Your product, \"" + product.title + "\" has been successfully added. Image less than/greater than 500x500 have been upsized/downsized and cropped to the middle and center.")
            return redirect(add_product_view)

@never_cache
@login_required
def add_to_cart_view(request, id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=id)
            user = User.objects.get(id=request.user.id)
            if product.bought == True:
                messages.add_message(request, messages.ERROR, mark_safe("<li>Sorry, this product, \"" + product.title + "\" is now sold out.</li>"))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif product.lister == user:
                messages.add_message(request, messages.ERROR, mark_safe("<li>You cannot add your own product to the cart.</li>"))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif Cart.objects.filter(product=product, user=user).exists():
                messages.add_message(request, messages.ERROR, mark_safe("<li>This product, \"" + product.title + "\" already exist in your cart.</li>"))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                cart = Cart(product=product, user=user)
                cart.save()
                messages.add_message(request, messages.SUCCESS, "You've successfully added, \"" + product.title + "\", to your cart.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except (Product.DoesNotExist, User.DoesNotExist, Cart.DoesNotExist):
            messages.add_message(request, messages.ERROR, mark_safe("<li>There seems to be an error in adding this product to your cart.</li>"))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@never_cache
@login_required
def remove_from_cart_view(request, id):
    if request.method == "POST":
        try:
            item = Cart.objects.get(id=id)
            item.delete()
            messages.add_message(request, messages.SUCCESS, "The item, \"" + item.product.title + "\", has been successfully removed from your cart.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Cart.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<li>There seems to be an error in remove this item from your cart.</li>"))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@never_cache
@login_required
def cart_view(request):
    if request.method == "GET":
        try:
            user = User.objects.get(id=request.user.id)
            cart = Cart.objects.filter(user=user)
        except (Cart.DoesNotExist, User.DoesNotExist):
            cart = None
        return render(request, 'cart.html', { 'cart': cart })

@never_cache
@login_required
def check_out_view(request):
    if request.method == "POST":
        already_bought = 0
        user = User.objects.get(id=request.user.id)
        cart = Cart.objects.filter(user=user)
        for item in cart:
            product = Product.objects.get(id=item.product.id)
            if product.bought == False:    
                product.bought = True
                product.save()
                sold = Sold(product=product, buyer=user)
                sold.save()
                item.delete()
            else:
                already_bought = already_bought + 1
        if already_bought == 0:
            messages.add_message(request, messages.SUCCESS, "Checkout was successful. All the items in your cart have been bought by you.")
            return redirect(cart_view)
        elif already_bought == 1:
            if (cart.count() == already_bought):
                messages.add_message(request, messages.ERROR, mark_safe("<li>Checkout was unsuccessful. The item you wanted to buy has been bought by another person.</li>"))
                return redirect(cart_view)
            else:
                messages.add_message(request, messages.SUCCESS, "Checkout was successful. However, there was 1 item that has been bought by another person and that item is now marked by \"SOLD OUT\". That 1 item will not be purchased.")
                return redirect(cart_view)
        else:
            if (cart.count() == already_bought):
                messages.add_message(request, messages.ERROR, mark_safe("<li>Checkout was unsuccessful. The item(s) you wanted to buy has been bought by another person.</li>"))
                return redirect(cart_view)
            else:
                messages.add_message(request, messages.SUCCESS, "Checkout was successful. However, some item(s) has been bought by another person and those item(s) are now marked by \"SOLD OUT\". There was a total of " + str(already_bought) + " item(s) bought already. Those item(s) will not be purchased.")
                return redirect(cart_view)
        
@never_cache
@login_required
def confirm_message(request, type):
    if request.method == "GET":
        if type == "check-out":
            messages.add_message(request, messages.WARNING, "Are you sure you want to proceed with check out?")
            return redirect(cart_view)

@never_cache
@login_required
def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout successful!")
    return redirect(login_view)

def get_form_errors(form):
    errors = list(form.errors.values())
    error_string = ""
    for i in range(len(errors)):
        error_string = error_string + "<li>" + str(list(form.errors.values())[i][0]) + "</li>"
    return error_string