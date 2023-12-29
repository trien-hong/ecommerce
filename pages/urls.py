from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('reset-password/', views.reset_password_view, name='reset_password_view'),
    path('index/', views.index_view, name='index_view'),
    path('product/id/<int:id>/', views.product_view, name='product_view'),
    path('add-product/', views.add_product_view, name='add_product_view'),
    path('add-to-cart/id/<int:id>/', views.add_to_cart_view, name='add_to_cart_view'),
    path('remvoe-from-cart/id/<int:id>/', views.remove_from_cart_view, name='remove_from_cart_view'),
    path('cart/', views.cart_view, name='cart_view'),
    path('check-out/', views.check_out_view, name='check_out_view'),
    path('logout_user/', views.logout_user, name='logout_user'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)