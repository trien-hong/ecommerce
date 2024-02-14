import os
from uuid import uuid4
from django.http import HttpResponseRedirect
from django.db.models.functions import Lower
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from . import forms
from .models import Product
from .models import Cart
from .models import Sold
from .choices import Choices # to see or edit the choices go to choices.py
User = get_user_model()

@never_cache
def login_view(request):
    """
    URL: /login
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(index_view)
        else:
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
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>The username and/or password seems to be incorrect.</li><li>Please try agian.</li></ul>"))
                return redirect(login_view)
        else:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>The username and/or password seems to be incorrect.</li><li>Please try agian.</li></ul>"))
            return redirect(login_view)

@never_cache
def signup_view(request):
    """
    URL: /signup
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(index_view)
        else:
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
            messages.add_message(request, messages.ERROR, signup_form.errors)
            return redirect(signup_view)

@never_cache
def reset_password_view(request):
    """
    URL: /reset-password
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(index_view)
        else:
            reset_password_form = forms.RestPassword()
            return render(request, "reset_password.html", { "reset_password_form": reset_password_form})
    if request.method == "POST":
        user_info = request.POST
        reset_password_form = forms.RestPassword(user_info)
        if reset_password_form.is_valid():
            # i hope to one day add verfication to this before users are allowed to actually change it
            user = User.objects.get(username=reset_password_form.cleaned_data["username"])
            user.set_password(reset_password_form.cleaned_data["confirm_password"])
            user.save()
            messages.add_message(request, messages.SUCCESS, "The password associated with the username has been reset. You may now login.")
            return redirect(reset_password_view)
        else:
            messages.add_message(request, messages.ERROR, reset_password_form.errors)
            return redirect(reset_password_view)

@never_cache
@login_required
def index_view(request):
    """
    URL: /index OR ""
    Query strings for filtering: ?all-products=..., ?category=..., ?condition=... and ... is one of the following choices (see choices.py/filter_by.html)
    Query strings for sorting: ?title=..., ?date=..., ?views=..., and ... is either ascending or descending
    Query string for pagination: ?page=... and ... is a number
    """
    if request.method == "GET":
        user = request.user
        all_products = request.GET.get("all-products", None)
        category = request.GET.get("category", None)
        condition = request.GET.get("condition", None)
        title = request.GET.get("title", None)
        date = request.GET.get("date", None)
        views = request.GET.get("views", None)
        page_number = request.GET.get("page", 1)
        filter_by = None
        sort_by = None
        search_product_form = forms.SearchProduct()
        products = Product.objects.all().exclude(status=Choices.CHOICES_PRODUCT_STATUS[2][0]).exclude(status=Choices.CHOICES_PRODUCT_STATUS[3][0]).order_by(Lower("title")) # to see or edit the choices go to choices.py
        if all_products is not None:
            if all_products == "True":
                filter_by = ["all-products=true", "All Products"]
            else:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error with the filtering.</li><li>Please try again.</li></ul>"))
        elif category is not None:
            if category != "":
                filter_by = ["category=" + category, "Category - " + category]
                products = products.filter(category=category)
            else:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error with filtering by category.</li><li>Please try again.</li></ul>"))
        elif condition is not None:
            if condition != "":
                filter_by = ["condition=" + condition, "Condition - " + condition]
                products = products.filter(condition=condition)
            else:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error with filtering by condition.</li><li>Please try again.</li></ul>"))
        if title is not None:
            if title == "ascending":
                sort_by = ["title=ascending", "Title (A - Z)"]
                products = products.order_by(Lower("title"))
            elif title == "descending":
                sort_by = ["title=descending", "Title (Z - A)"]
                products = products.order_by(Lower("title").desc())
            else:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error with sorting by title.</li><li>Please try again.</li></ul>"))
        elif date is not None:
            if date == "ascending":
                sort_by = ["date=ascending", "Date (Low - High)"]
                products = products.order_by("list_date")
            elif date == "descending":
                sort_by = ["date=descending", "Date (High - Low)"]
                products = products.order_by("-list_date")
            else:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error with sorting by date.</li><li>Please try again.</li></ul>"))
        elif views is not None:
            if views == "ascending":
                sort_by = ["views=ascending", "Views (Low - High)"]
                products = products.order_by("views")
            elif views == "descending":
                sort_by = ["views=descending", "Views (High - Low)"]
                products = products.order_by("-views")
            else:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error with sorting by views.</li><li>Please try again.</li></ul>"))
        products = Paginator(products, 9).page(page_number)
        # cart = Cart.objects.filter(user=user)
        # items_in_cart = products.filter(uuid__in=cart.values_list("product__uuid", flat=True))
        # products = Paginator(products.difference(items_in_cart), 9).page(page_number)
        # it has come to my attention that .difference(...) does not work on either side of .order_by(...)
        # for the time being, i'll remove it and possibly find a different solution later
        # items within cart will now reappear on the index page
        return render(request, "index.html", { "current_username": user.username, "products": products, "filter_by": filter_by, "sort_by": sort_by, "current_page_number": page_number,"search_product_form": search_product_form })

@never_cache
@login_required
def product_view(request, uuid):
    """
    URL: /product/id/<uuid:uuid>
    where <uuid:uuid> is the uuid (NOT ID despite the URL) of the product being viewed
    if exposed the uuid is shown to the user and not the ID/PK
    """
    if request.method == "GET":
        try:
            user = request.user
            product = Product.objects.get(uuid=uuid)
            if product.seller != user:
                product.views = product.views + 1
                product.save()
            if Cart.objects.filter(product=product, user=user).exists():
                in_cart = True
            else:
                in_cart = False
        except Product.DoesNotExist:
            product = None
            in_cart = False
        return render(request, "product.html", { "current_username": user.username, "product": product, "in_cart": in_cart })

@never_cache
@login_required
def add_product_view(request):
    """
    URL: /product/add-product
    """
    if request.method == "GET":
        user = request.user
        option = request.GET.get("option", None)
        upc = request.GET.get("upc", None)
        ean = request.GET.get("upc", None)
        if option == "manually":
            add_product_form = forms.AddProduct()
            return render(request, "add_product.html", { "add_product_form": add_product_form, "option": "manually"})
        elif option == "upc-ean-lookup":
            upc_ean_lookup_form = forms.UpcEanLookup()
            return render(request, "add_product.html", { "upc_ean_lookup_form": upc_ean_lookup_form, "option": "upc_ean_lookup" })
        elif upc is not None or ean is not None:
            upc_ean_lookup_form = forms.UpcEanLookup(request.GET)
            products = None
            if upc_ean_lookup_form.is_valid():
                if upc_ean_lookup_form.cleaned_data["upc"] != "" and upc_ean_lookup_form.cleaned_data["ean"] == "":
                    products = Product.objects.filter(upc=upc_ean_lookup_form.cleaned_data["upc"])
                elif upc_ean_lookup_form.cleaned_data["ean"] != "" and upc_ean_lookup_form.cleaned_data["upc"] == "":
                    products = Product.objects.filter(ean=upc_ean_lookup_form.cleaned_data["ean"])
                elif upc_ean_lookup_form.cleaned_data["upc"] != "" and upc_ean_lookup_form.cleaned_data["ean"] != "":
                    products = Product.objects.filter(upc=upc_ean_lookup_form.cleaned_data["upc"], ean=upc_ean_lookup_form.cleaned_data["ean"])
                if products.exists() is False:
                    messages.add_message(request, messages.ERROR, mark_safe("<ul><li>The UPC and/or EAN did not match a record on our database.</li><li>Please try again.</li></ul>"))
                return render(request, "add_product.html", { "upc_ean_lookup_form": upc_ean_lookup_form, "products": products, "option": "upc_ean_lookup" })
            else:
                messages.add_message(request, messages.ERROR, upc_ean_lookup_form.errors)
                return render(request, "add_product.html", { "upc_ean_lookup_form": upc_ean_lookup_form, "option": "upc_ean_lookup" })
        else:
            return render(request, "add_product.html", { "option": "how" })
    if request.method == "POST":
        user = request.user
        product_info = request.POST
        picture = request.FILES
        add_product_form = forms.AddProduct(product_info, picture)
        if add_product_form.is_valid():
            file_extension = add_product_form.cleaned_data["picture"].name.split(".")[-1]
            add_product_form.cleaned_data["picture"].name = "product_picture_id_" + str(uuid4()) + "." + file_extension
            product = Product(title=add_product_form.cleaned_data["title"], picture=add_product_form.cleaned_data["picture"], description=add_product_form.cleaned_data["description"], category=add_product_form.cleaned_data["category"], condition=add_product_form.cleaned_data["condition"], price=add_product_form.cleaned_data["price"], upc=add_product_form.cleaned_data["upc"], ean=add_product_form.cleaned_data["ean"], seller=user)
            product.save()
            messages.add_message(request, messages.SUCCESS, "Your product, \"" + product.title + "\" has been successfully added. Image less than/greater than 500x500 have been upsized/downsized and cropped to the middle and center.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.add_message(request, messages.ERROR, add_product_form.errors)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@never_cache
@login_required
def copy_and_add_product_view(request, uuid):
    """
    URL: /product/copy-product/id/<uuid:uuid>
    where <uuid:uuid> is the uuid (NOT ID despite the URL) of the product that you want to copy
    if exposed the uuid is shown to the user and not the ID/PK
    """
    if request.method == "GET":
        return redirect(add_product_view)
    if request.method == "POST":
        user = request.user
        try:
            original_product = Product.objects.get(uuid=uuid)
            product = Product(title=original_product.title, picture=original_product.picture, description=original_product.description, category=original_product.category, condition=original_product.condition, upc=original_product.upc, ean=original_product.ean, seller=user)
            product.save()
            messages.add_message(request, messages.SUCCESS, "This product's details has been copied over and a new listing has been created. Know that you may edit the product's details at any time.")
        except Product.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in copying this product's details.</li><li>Please try again.</li></ul>"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@never_cache
@login_required
def delete_product_view(request, uuid):
    """
    URL: /product/delete-product/id/<uuid:uuid>
    where <uuid:uuid> is the uuid (NOT ID despite the URL) of the product that you want to delete
    if exposed the uuid is shown to the user and not the ID/PK
    """
    if request.method == "GET":
        return redirect(profile_option_view, option="listing-history")
    if request.method == "POST":
        user = request.user
        try:
            product = Product.objects.get(uuid=uuid)
            if product.seller != user or product.status == Choices.CHOICES_PRODUCT_STATUS[3][0]: # to see or edit the choices go to choices.py
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in deleting this product from your profile.</li><li>Please try again.</li></ul>"))
            else:
                if os.path.exists(product.picture.path):
                    os.remove(product.picture.path)
                product.delete()
                messages.add_message(request, messages.SUCCESS, "You successfully deleted the product, \"" + product.title + "\", from your profile.")
        except Product.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in deleting this product from your profile.</li><li>Please try again.</li></ul>"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@never_cache
@login_required
def edit_product_view(request, uuid):
    """
    URL: /product/edit-product/id/<uuid:uuid>
    where <uuid:uuid> is the uuid (NOT ID despite the URL) of the product that you want to edit
    if exposed the uuid is shown to the user and not the ID/PK
    """
    if request.method == "GET":
        user = request.user
        edit_product_form = forms.EditProduct()
        try:
            product = Product.objects.get(uuid=uuid)
            if product.seller != user or product.status == Choices.CHOICES_PRODUCT_STATUS[3][0]: # to see or edit the choices go to choices.py
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
                product = Product.objects.get(uuid=uuid)
                if edit_product_form.cleaned_data["title"] == "" and edit_product_form.cleaned_data["picture"] is None and edit_product_form.cleaned_data["description"] == "" and edit_product_form.cleaned_data["category"] == "" and edit_product_form.cleaned_data["condition"] == "" and edit_product_form.cleaned_data["upc"] == "" and edit_product_form.cleaned_data["ean"] == "" and edit_product_form.cleaned_data["status"] == "":
                    messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Seems like you submitted an empty form.</li><li>If you have nothing to edit on the product, please don't edit it.</li></ul>"))
                else:
                    if edit_product_form.cleaned_data["title"] != "":
                        product.title = edit_product_form.cleaned_data["title"]
                    if edit_product_form.cleaned_data["picture"] is not None:
                        if os.path.exists(product.picture.path):
                            os.remove(product.picture.path)
                        file_extension = edit_product_form.cleaned_data["picture"].name.split(".")[-1]
                        edit_product_form.cleaned_data["picture"].name = "product_picture_id_" + str(uuid4()) + "." + file_extension
                        product.picture = edit_product_form.cleaned_data["picture"]
                    if edit_product_form.cleaned_data["description"] != "":
                        product.description = edit_product_form.cleaned_data["description"]
                    if edit_product_form.cleaned_data["category"] != "":
                        product.category = edit_product_form.cleaned_data["category"]
                    if edit_product_form.cleaned_data["condition"] != "":
                        product.condition = edit_product_form.cleaned_data["condition"]
                    if edit_product_form.cleaned_data["upc"] != "":
                        product.upc = edit_product_form.cleaned_data["upc"]
                    if edit_product_form.cleaned_data["ean"] != "":
                        product.ean = edit_product_form.cleaned_data["ean"]
                    if edit_product_form.cleaned_data["status"] != "":
                        product.status = edit_product_form.cleaned_data["status"]
                    product.save()
                    messages.add_message(request, messages.SUCCESS, "Your product have been successfully updated.")
            except Product.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in editing your product.</li><li>Please try again.</li></ul>"))
            return redirect(edit_product_view, uuid)
        else:
            messages.add_message(request, messages.ERROR, edit_product_form.errors)
            return redirect(edit_product_view, uuid)

@never_cache
@login_required
def edit_product_delete_upc_ean_view(request, uuid, type):
    """
    URL: product/edit-product/id/<uuid:uuid>/delete-<str:type>
    where <uuid:uuid> is the uuid (NOT ID despite the URL) of the product that you want to delete it's UPC/EAN from and where <str:type> is either upc or ean
    if exposed the uuid is shown to the user and not the ID/PK
    """
    if request.method == "GET":
        return redirect(edit_product_view, uuid)
    if request.method == "POST":
        user = request.user
        try:
            product = Product.objects.get(uuid=uuid)
            if product.seller != user or product.status == Choices.CHOICES_PRODUCT_STATUS[3][0]: # to see or edit the choices go to choices.py
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in deleting the product's UPC/EAN.</li><li>Please try again.</li></ul>"))
                return redirect(edit_product_view, uuid)
            else:
                if type == "upc":
                    product.upc = ""
                    product.save()
                    messages.add_message(request, messages.SUCCESS, "You successfully deleted the product's UPC.")
                elif type == "ean":
                    product.ean = ""
                    product.save()
                    messages.add_message(request, messages.SUCCESS, "You successfully deleted the product's EAN.")
                else:
                    messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in deleting the product's UPC/EAN.</li><li>Please try again.</li></ul>"))
        except Product.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in deleting the product's UPC/EAN.</li><li>Please try again.</li></ul>"))
        return redirect(edit_product_view, uuid)

@never_cache
@login_required
def search_view(request):
    """
    URL: /products/search?title=...
    where title=... is the query string
    """
    if request.method == "GET":
        user = request.user
        search = request.GET
        search_product_form = forms.SearchProduct(search)
        if search_product_form.is_valid():
            if search_product_form.cleaned_data["title"] == "":
                products = None
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Sorry, your search of, \"" + search_product_form.cleaned_data["title"] + "\", came by empty.</li><li>Please note that you are searching by title.</li></ul>"))
            else:
                products = Product.objects.filter(title__istartswith=search_product_form.cleaned_data["title"]).exclude(status=Choices.CHOICES_PRODUCT_STATUS[2][0]).exclude(status=Choices.CHOICES_PRODUCT_STATUS[3][0]) # to see or edit the choices go to choices.py
                if products.exists() is False:
                    products = Product.objects.filter(title__icontains=search_product_form.cleaned_data["title"]).exclude(status=Choices.CHOICES_PRODUCT_STATUS[2][0]).exclude(status=Choices.CHOICES_PRODUCT_STATUS[3][0]) # to see or edit the choices go to choices.py
                if products.exists() is False:
                    messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Sorry, your search of, \"" + search_product_form.cleaned_data["title"] + "\", came by empty.</li><li>Please note that you are searching by title.</li></ul>"))
                else:
                    cart = Cart.objects.filter(user=user)
                    items_in_cart = products.filter(uuid__in=cart.values_list("product__uuid", flat=True))
                    products = products.difference(items_in_cart)
                    messages.add_message(request, messages.SUCCESS, "Your search resulted in " + str(products.count()) + " products.")
            return render(request, "search.html", { "current_username": user.username, "products": products, "search_product_form": search_product_form, "search_term": search_product_form.cleaned_data["title"] })
        else:
            messages.add_message(request, messages.ERROR, search_product_form.errors)
            return render(request, "search.html", { "search_product_form", search_product_form })

@never_cache
@login_required
def advanced_search_view(request):
    """
    URL: /products/advance-search?title=...&category=...&condition=...&upc=...&ean=...&seller=...
    where title=...&category=...&condition=...&upc=...&ean=...&seller=... is the query string
    """
    if request.method == "GET":
        user = request.user
        advanced_search_product_form = forms.AdvancedSearchProduct(request.GET)
        if advanced_search_product_form.is_valid():
            try:
                if (advanced_search_product_form.cleaned_data["title"] == "" or advanced_search_product_form.cleaned_data["title"] is None) and (advanced_search_product_form.cleaned_data["category"] == "" or advanced_search_product_form.cleaned_data["category"] is None) and (advanced_search_product_form.cleaned_data["condition"] == "" or advanced_search_product_form.cleaned_data["condition"] is None) and (advanced_search_product_form.cleaned_data["upc"] == "" or advanced_search_product_form.cleaned_data["upc"] is None) and (advanced_search_product_form.cleaned_data["ean"] == "" or advanced_search_product_form.cleaned_data["ean"] is None) and (advanced_search_product_form.cleaned_data["username"] == "" or advanced_search_product_form.cleaned_data["username"] is None):
                    products = None
                else:
                    # products = Product.objects.filter(title=..., category=..., condition=..., upc=..., ean=..., seller=...).exclude(status=Choices.CHOICES_PRODUCT_STATUS[2][0]).exclude(status=Choices.CHOICES_PRODUCT_STATUS[3][0])
                    # where ... does not work with "" (empty string) or None
                    products = Product.objects.all().exclude(status=Choices.CHOICES_PRODUCT_STATUS[2][0]).exclude(status=Choices.CHOICES_PRODUCT_STATUS[3][0]) # to see or edit the choices go to choices.py
                    if advanced_search_product_form.cleaned_data["title"] != "" and advanced_search_product_form.cleaned_data["title"] is not None:
                        products = products.filter(title__istartswith=advanced_search_product_form.cleaned_data["title"])
                    if advanced_search_product_form.cleaned_data["category"] != "" and advanced_search_product_form.cleaned_data["category"] is not None:
                        products = products.filter(category=advanced_search_product_form.cleaned_data["category"])
                    if advanced_search_product_form.cleaned_data["condition"] != "" and advanced_search_product_form.cleaned_data["condition"] is not None:
                        products = products.filter(condition=advanced_search_product_form.cleaned_data["condition"])
                    if advanced_search_product_form.cleaned_data["upc"] != "" and advanced_search_product_form.cleaned_data["upc"] is not None:
                        products = products.filter(upc=advanced_search_product_form.cleaned_data["upc"])
                    if advanced_search_product_form.cleaned_data["ean"] != "" and advanced_search_product_form.cleaned_data["ean"] is not None:
                        products = products.filter(ean=advanced_search_product_form.cleaned_data["ean"])
                    if advanced_search_product_form.cleaned_data["username"] != "" and advanced_search_product_form.cleaned_data["username"] is not None:
                        if User.objects.filter(username=advanced_search_product_form.cleaned_data["username"]).exists():
                            seller = User.objects.get(username=advanced_search_product_form.cleaned_data["username"])
                            products = products.filter(seller=seller)
                        else:
                            products = None
                    if products is None or products.count() == 0:
                        messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Your advanced search resulted in 0 products.</li><li>Please try again.</li></ul>"))
                    else:
                        cart = Cart.objects.filter(user=user)
                        items_in_cart = products.filter(uuid__in=cart.values_list("product__uuid", flat=True))
                        products = products.difference(items_in_cart)
                        messages.add_message(request, messages.SUCCESS, "Your search resulted in " + str(products.count()) + " products.")
            except:
                products = None
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error with your advanced search.</li><li>Please try again.</li></ul>"))
            return render (request, "advanced_search.html", { "current_username": user.username, "advanced_search_product_form": advanced_search_product_form, "products": products })
        else:
            products = None
            messages.add_message(request, messages.ERROR, advanced_search_product_form.errors)
            return render (request, "advanced_search.html", { "current_username": user.username, "advanced_search_product_form": advanced_search_product_form, "products": products })

@never_cache
@login_required
def cart_view(request):
    """
    URL: /cart
    """
    if request.method == "GET":
        user = request.user
        cart = Cart.objects.filter(user=user)
        total_price = Product.objects.filter(uuid__in=cart.values_list("product__uuid", flat=True)).aggregate(Sum('price'))["price__sum"]
        return render(request, "cart.html", { "cart": cart, "total_price": total_price })

@never_cache
@login_required
def add_to_cart_view(request, uuid):
    """
    URL: /cart/add-to-cart/id/<uuid:uuid>
    where <uuid:uuid> is the uuid (NOT ID/PK despite the URL) of product being added to the cart
    if exposed the uuid is shown to the user and not the ID/PK
    """
    if request.method == "GET":
        return redirect(product_view, uuid=uuid)
    if request.method == "POST":
        try:
            user = request.user
            product = Product.objects.get(uuid=uuid)
            if product.status == Choices.CHOICES_PRODUCT_STATUS[3][0]: # to see or edit the choices go to choices.py
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Sorry, this product, \"" + product.title + "\" is now sold out.</li></ul>"))
            elif product.seller == user:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>You cannot add your own product to the cart.</li></ul>"))
            elif Cart.objects.filter(product=product, user=user).exists():
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>This product, \"" + product.title + "\" already exist in your cart.</li></ul>"))
            else:
                cart = Cart(product=product, user=user)
                cart.save()
                messages.add_message(request, messages.SUCCESS, "You've successfully added, \"" + product.title + "\", to your cart.")
        except Product.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in adding this product to your cart.</li></ul>"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@never_cache
@login_required
def delete_from_cart_view(request, uuid):
    """
    URL: /cart/delete-from-cart/id/<uuid:uuid>
    where <uuid:uuid> is the uuid (NOT ID/PK despite the URL) of item being removed from the cart
    if exposed the uuid is shown to the user and not the ID/PK
    """
    if request.method == "GET":
        return redirect(cart_view)
    if request.method == "POST":
        try:
            item = Cart.objects.get(uuid=uuid)
            item.delete()
            messages.add_message(request, messages.SUCCESS, "The product, \"" + item.product.title + "\", has been successfully removed from your cart.")
        except Cart.DoesNotExist:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in removing this product from your cart.</li></ul>"))
        return redirect(cart_view)

@never_cache
@login_required
def delete_all_items_from_cart_view(request):
    """
    URL: /cart/delete-all-items-from-cart
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
    URL: /cart/check-out
    """
    if request.method == "GET":
        return redirect(cart_view)
    if request.method == "POST":
        user = request.user
        cart = Cart.objects.filter(user=user)
        total_price = Product.objects.filter(uuid__in=cart.values_list("product__uuid", flat=True)).aggregate(Sum('price'))["price__sum"]
        if total_price > request.user.credits:
            messages.add_message(request, messages.ERROR, mark_safe("<ul><li>You do not have enough credits to purchase all these items within your cart.</li></ul>"))
            return redirect(cart_view)
        else:
            already_bought = 0
            for item in cart:
                try:
                    product = Product.objects.get(id=item.product.id)
                    if product.status != Choices.CHOICES_PRODUCT_STATUS[3][0]: # to see or edit the choices go to choices.py
                        seller = User.objects.get(username=product.seller)
                        seller.credits = seller.credits + product.price
                        seller.save()
                        buyer = User.objects.get(username=user.username)
                        buyer.credits = buyer.credits - product.price
                        buyer.save()
                        sold = Sold(product=product, buyer=user)
                        sold.save()
                        product.status = Choices.CHOICES_PRODUCT_STATUS[3][0] # to see or edit the choices go to choices.py
                        product.save()
                        item.delete()
                    else:
                        already_bought = already_bought + 1
                except Product.DoesNotExist:
                    messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error with one, some, or all your items in your cart.</li><li>It's possible the seller delisted an item in your cart.</li></ul>"))
                    return redirect(cart_view)
            if already_bought == 0:
                messages.add_message(request, messages.SUCCESS, "Checkout was successful. All the items in your cart have been bought by you.")
                return redirect(cart_view)
            elif already_bought == 1:
                if cart.count() == already_bought:
                    messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Checkout was unsuccessful.</li><li>The item you wanted to buy has been bought by another person.</li></ul>"))
                    return redirect(cart_view)
                else:
                    messages.add_message(request, messages.SUCCESS, "Checkout was successful. However, there was 1 item that has been bought by another person and that item is now marked by \"SOLD OUT\". That 1 item will not be purchased.")
                    return redirect(cart_view)
            else:
                if cart.count() == already_bought:
                    messages.add_message(request, messages.ERROR, mark_safe("<ul><li>Checkout was unsuccessful.</li><li>The item(s) you wanted to buy has been bought by another person.</li></ul>"))
                    return redirect(cart_view)
                else:
                    messages.add_message(request, messages.SUCCESS, "Checkout was successful. However, some item(s) has been bought by another person and those item(s) are now marked by \"SOLD OUT\". There was a total of " + str(already_bought) + " item(s) bought already. Those item(s) will not be purchased.")
                    return redirect(cart_view)

@never_cache
@login_required
def profile_view(request):
    """
    URL: /profile
    """
    if request.method == "GET":
        user = request.user
        return render(request, "profile.html", { "current_username": user.username, "available_credits": user.credits, "option": None })

@never_cache
@login_required
def profile_option_view(request, option):
    """
    URL: /profile/<str:option>
    where <str:option> is either "settings", "wish-list", "listing-history", "purchase-history", or "login-history" and if not simply redirect to profile page
    """
    if request.method == "GET":
        user = request.user
        if option == "settings":
            change_username_form = forms.ChangeUsername()
            change_password_form = forms.ChangePassword()
            delete_account_form = forms.DeleteAccount()
            return render(request, "profile.html", { "current_username": user.username, "available_credits": user.credits, "option": "settings", "change_username_form": change_username_form, "change_password_form": change_password_form, "delete_account_form": delete_account_form })
        elif option == "wish-list":
            return render(request, "profile.html", { "current_username": user.username, "available_credits": user.credits, "option": "wish-list" })
        elif option == "listing-history":
            listing_history = Product.objects.filter(seller=user)
            return render(request, "profile.html", { "current_username": user.username, "available_credits": user.credits, "option": "listing-history", "listing_history": listing_history })
        elif option == "purchase-history":
            purchase_history = Sold.objects.filter(buyer=user)
            return render(request, "profile.html", { "current_username": user.username, "available_credits": user.credits, "option": "purchase-history", "purchase_history": purchase_history })
        elif option == "login-history":
            return render(request, "profile.html", { "current_username": user.username, "available_credits": user.credits, "option": "login-history" })
        else:
            return redirect(profile_view)

@never_cache
@login_required
def change_username_view(request):
    """
    URL: /profile/settings/change-username
    """
    if request.method == "GET":
        return redirect(profile_option_view, option="settings")
    if request.method == "POST":
        user_info = request.POST
        change_username_form = forms.ChangeUsername(user_info)
        if change_username_form.is_valid():
            try:
                # i hope to one day add verfication to this before users are allowed to actually change it
                user = User.objects.get(id=request.user.id)
                user.username = change_username_form.cleaned_data["username"]
                user.save()
                messages.add_message(request, messages.SUCCESS, "Your username is now \"" + change_username_form.cleaned_data["username"] +"\". Everything associated with the username has now been updated.")
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in updating your username.</li><li>Please try again.</li></ul>"))
            return redirect(profile_option_view, option="settings")
        else:
            messages.add_message(request, messages.ERROR, change_username_form.errors)
            return redirect(profile_option_view, option="settings")

@never_cache
@login_required
def change_password_view(request):
    """
    URL: /profile/settings/change-password
    """
    if request.method == "GET":
        return redirect(profile_option_view, option="settings")
    if request.method == "POST":
        user_info = request.POST
        change_password_form = forms.ChangePassword(user_info)
        if change_password_form.is_valid():
            try:
                # i hope to one day add verfication to this before users are allowed to actually change it
                user = User.objects.get(id=request.user.id)
                user.set_password(change_password_form.cleaned_data["password"])
                user.save()
                messages.add_message(request, messages.SUCCESS, "Your password has been successfully updated. You must login again with the new password.")
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in updating your password.</li><li>Please try again.</li></ul>"))
            return redirect(profile_option_view, option="settings")
        else:
            messages.add_message(request, messages.ERROR, change_password_form.errors)
            return redirect(profile_option_view, option="settings")

@never_cache
@login_required
def delete_account_view(request):
    """
    URL: /profile/settings/delete-account
    """
    if request.method == "GET":
        return redirect(profile_option_view, option="settings")
    if request.method == "POST":
        user_info = request.POST
        delete_account_form = forms.DeleteAccount(user_info, user=request.user)
        if delete_account_form.is_valid():
            try:
                # i hope to one day add verfication to this before users are allowed to actually change it
                user = User.objects.get(id=request.user.id)
                user.delete()
                messages.add_message(request, messages.SUCCESS, "Your account has been deleted. Thank you for using our service!")
                return redirect(login_view)
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, mark_safe("<ul><li>There seems to be an error in deleting your account.</li><li>Please try again.</li></ul>"))
                return redirect(profile_option_view, option="settings")
        else:
            messages.add_message(request, messages.ERROR, delete_account_form.errors)
            return redirect(profile_option_view, option="settings")

@never_cache
@login_required
def confirm_message_view(request, type):
    """
    URL: /confirm-message/type/<str:type>
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
        elif type == "delete-upc":
            messages.add_message(request, messages.WARNING, "Are you sure you want to delete the UPC tied to this product?", extra_tags="delete-upc")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        elif type == "delete-ean":
            messages.add_message(request, messages.WARNING, "Are you sure you want to delete the EAN tied to this product?", extra_tags="delete-ean")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            return redirect(index_view)

@never_cache
@login_required
def logout_user(request):
    """
    URL: /logout-user
    """
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout successful!")
    return redirect(login_view)
