from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path

from apps.views import add_product, register, ProductList, AddWishlist, \
    ProductDetailView

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/<int:pk>', AddWishlist.as_view(), name='add_wishlist'),
    path('add_product', add_product, name='add_product'),

    path('register', register, name='register'),
    path('login', LoginView.as_view(
        next_page='product_list',
        template_name='apps/auth/login.html',
    ), name='login_page'),
    path('logout', LogoutView.as_view(
        next_page='product_list'
    ), name='logout_page'),
    path('password-reset', PasswordResetView.as_view(
        template_name='apps/auth/password_reset.html'
    ), name='password_reset'),
]
