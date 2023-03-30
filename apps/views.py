from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, PasswordResetView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from apps.forms import UsersCreationForm, ProductForm
from apps.models import Product, ProductImage, Wishlist


def register(request):
    context = {
        'form': UsersCreationForm()
    }
    if request.method == 'POST':
        form = UsersCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_page')
        context['form'] = form
    return render(request, 'apps/auth/register.html', context)


# def login_page(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         user = authenticate(username=form.data['username'], password=form.data['password'])
#         if user is not None:
#             login(request, user)
#             return redirect('product_list')
#     return render(request, 'apps/auth/login.html')


# def logout_page(request):
#     logout(request)
#     return redirect('product_list')
#     # return render(request, 'apps/auth/logout.html')

#
# def forgot(request):
#     return render(request, 'apps/auth/forgot_password.html')


class AddWishlist(LoginRequiredMixin, View):
    def get(self, request, pk):
        wishlist, created = Wishlist.objects.get_or_create(product_id=pk, user=request.user)
        if not created:
            wishlist.delete()

        return redirect('product_list')


class ProductList(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_grid.html'
    context_object_name = 'products'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     context['name'] = 'Botirjon'
    #     return context


# def product_list(request):
#     products = Product.objects.all()
#     context = {
#         'products': products
#     }
#     return render(request, 'apps/product/product_grid.html', context)

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_detail.html'
    context_object_name = 'product'


# def product_detail(request, pk=None):
#     image = ProductImage.objects.filter(product_id=pk)
#     product = Product.objects.get(id=pk)
#     context = {
#         'product': product,
#         'image': image
#     }
#     return render(request, 'apps/product/product_details.html', context)


@permission_required('apps.add_product')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            product = form.save()
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(image=image, product=product)

        return redirect('/')
    return render(request, 'apps/product/add-product.html')
