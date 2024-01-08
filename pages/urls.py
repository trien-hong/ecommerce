from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("index/", views.index_view, name="index_view"),
    path("login/", views.login_view, name="login_view"),
    path("signup/", views.signup_view, name="signup_view"),
    path("reset-password/", views.reset_password_view, name="reset_password_view"),
    path("product/id/<int:id>/", views.product_view, name="product_view"),
    path("add-product/", views.add_product_view, name="add_product_view"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add-to-cart/id/<int:id>/", views.add_to_cart_view, name="add_to_cart_view"),
    path("cart/delete-from-cart/id/<int:id>/", views.delete_from_cart_view, name="delete_from_cart_view"),
    path("cart/delete-all-items-from-cart/", views.delete_all_items_from_cart_view, name="delete_all_items_from_cart_view"),
    path("cart/check-out/", views.check_out_view, name="check_out_view"),
    path("profile/", views.profile_view, name="profile_view"),
    path("profile/<str:option>/", views.profile_option_view, name="profile_option_view"),
    path("profile/settings/change-username/", views.change_username_view, name="change_username_view"),
    path("profile/settings/change-password/", views.change_password_view, name="change_password_view"),
    path("profile/settings/delete-account/", views.delete_account_view, name="delete_account_view"),
    path("confirm-message/type/<str:type>/", views.confirm_message, name="confirm_message_view"),
    path("logout-user/", views.logout_user, name="logout_user"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)