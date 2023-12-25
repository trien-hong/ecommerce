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
    path('add-product/', views.add_product_view, name='add_product_view'),
    path('logout_user/', views.logout_user, name='logout_user'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)