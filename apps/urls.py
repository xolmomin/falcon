from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path
from django.conf.urls.static import static

from apps.views import add_product, register, ProductList, AddWishlist, \
    ProductDetailView, ShowCart, AddCartCreateView, ProductDeleteView
from core import settings

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/<int:pk>', AddWishlist.as_view(), name='add_wishlist'),
    path('add_product', add_product, name='add_product'),
    path('product-delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('cart', ShowCart.as_view(), name='cart'),
    path('add-cart/<int:pk>', AddCartCreateView.as_view(), name='add_cart')
]

urlpatterns += [
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

   path('password-reset-done', PasswordResetDoneView.as_view(
       template_name='apps/auth/password_reset_done.html'
   ), name='password_reset_done'),

   path('password-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(
       template_name='apps/auth/password_reset_confirm.html',
       success_url='product_list'
   ), name='password_reset_confirm'),

   # path('password-confirm', PasswordResetCompleteView.as_view(
   #     template_name='apps/auth/password_reset_done.html'
   # ), name='password_confirm'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
