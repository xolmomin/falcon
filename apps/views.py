from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from apps.forms import UsersCreationForm, ProductForm
from apps.models import Product, ProductImage, Wishlist, Tag, User, CartItem, Cart


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


class AddWishlist(LoginRequiredMixin, View):
    def get(self, request, pk):
        wishlist, created = Wishlist.objects.get_or_create(product_id=pk, user=request.user)
        if not created:
            wishlist.delete()

        return redirect('product_list')


class ProductList(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        user: User = self.request.user
        if user.is_authenticated and user.status != User.Status.CLIENT:
            return super().get_queryset()
        return Product.objects.filter(is_premium=False)


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_detail.html'
    context_object_name = 'product'


@permission_required('apps.add_product')
def add_product(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            product = form.save()
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(image=image, product=product)

        return redirect('/')
    return render(request, 'apps/product/add-product.html', {'tags': tags})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/'


# @permission_required('apps.add_product')
# def product_delete(request, pk):
#     user = request.user
#     article = Product.objects.get(id=pk)
#     if user == article.author:
#         if request.method == "POST":
#             article.delete()
#             return redirect('/')
#         return render(request, 'apps/product/product_detail.html', {"article": article})
#     else:
#         return HttpResponse("Not allowed")


class AddCartCreateView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        CartItem.objects.create(
            product=product,
            price=product.price,
            cart=cart
        )
        return redirect('product_list')


class ShowCart(ListView):
    queryset = CartItem.objects.all()
    template_name = 'apps/product/shopping-cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user, is_active=True).first()
        return CartItem.objects.filter(cart=cart)
