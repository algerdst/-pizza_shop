from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect, redirect
from django.views.generic import ListView

from common.views import ContextMixin

from .models import Basket, Category, Product


class IndexView(ContextMixin, ListView):
    model = Product
    template_name = 'home/index.html'
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories, 600)
    queryset = Product.objects.order_by('category')


class AboutProductDetailView(ContextMixin, ListView):
    model = Product
    template_name = 'home/about_product.html'
    categories = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AboutProductDetailView, self).get_context_data()
        context['products'] = Product.objects.filter(slug=self.kwargs.get('slug_name'))
        return context


class ProductsListView(ContextMixin, ListView):
    model = Product
    template_name = 'home/index.html'
    categories = Category.objects.all()

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        queryset = Product.objects.filter(category_id=category_id) if category_id \
            else Product.objects.order_by(
            'category')
        return queryset


def basket_add(request, product_id):
    if request.user.id is None:
        messages.error(request, 'Для использования корзины требуется авторизация')
        return redirect('home')
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)
    if not basket.exists():
        Basket(user=request.user, product=product, quantity=1).save()
    else:
        basket = basket[0]
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    Basket.delete(basket)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# Представления на функциях

# def index(request):
#     data = {
#         'products': Product.objects.order_by('category'),
#         'categories': Category.objects.all()
#     }
#     return render(request, 'home/index.html', context=data)


# def products(request, category_id=None,page_number=1):
#     if category_id:
#         category = Category.objects.get(id=category_id)
#         products = Product.objects.filter(category=category)
#     else:
#         products = Product.objects.order_by('category')
#     per_page = 3
#     paginator=Paginator(products,per_page)
#     products_paginator=paginator.page(page_number)
#     data = {
#         'products': products_paginator,
#         'categories': Category.objects.all()
#     }
#     return render(request, 'home/index.html', context=data)


# def about_product(request,slug_name):
#     products=Product.objects.filter(slug=slug_name)
#     data={
#         'products':products,
#         'categories': Category.objects.all()
#     }
#     return render(request,'home/about_product.html',data)
