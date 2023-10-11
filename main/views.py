import json

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView

from .form import ProductForm
from .models import ShoppingCart, Product, Picture
from .utls import increment_count, decrement_count
from django.contrib.auth.decorators import login_required


class HomeView(View):
    template_name = 'index.html'
    context = {}

    def get(self, request):
        products = Product.objects.all()[:4]
        product_data = []
        for product in products:
            image = Picture.objects.filter(product=product).first()
            product.image = image
            product_data.append(product)

        self.context.update({'products': product_data})
        return render(request, self.template_name, self.context)

    def post(self, request):
        id = request.POST.get('id')
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(Q(product_id=id) & Q(user=user))
        if not shopping_cart:
            shopping_cart = ShoppingCart.objects.create(
                product_id=id,
                user=user
            )
            shopping_cart.save()
            messages.info(request, "Added successfully!")
            return redirect('/')
        return redirect('/cart')


class ShoppingCartView(View):
    template_name = 'cart.html'
    context = {}

    def get(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user).values('product_id')
        products = Product.objects.filter(pk__in=shopping_cart)
        data = []
        for product in products:
            image = Picture.objects.filter(product=product).first()
            product.image = image
            shop = ShoppingCart.objects.get(Q(user=request.user) & Q(product=product))
            product.count = shop.count
            data.append(product)

        self.context.update({'products': data})
        return render(request, self.template_name, self.context)

    def post(self, request):
        id = request.POST.get('id')
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(Q(product_id=id) & Q(user=user))
        shopping_cart.delete()
        return redirect('/cart')


class IncrementCountView(View):
    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            id = json_data.get('id')
        except json.JSONDecodeError:
            id = None
        result = increment_count(id, request.user)
        return JsonResponse({'result': result})


class DecrementCountView(View):
    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            id = json_data.get('id')
        except json.JSONDecodeError:
            id = None
        result = decrement_count(id, request.user)
        return JsonResponse({'result': result})


def contact(request):
    return render(request, 'contact.html')


def detail(request):
    return render(request, 'detail.html')


class ShopView(View):
    def get(self, request):
        products = Product.objects.all()
        product_data = []
        for product in products:
            image = Picture.objects.filter(product=product).first()
            product.image = image
            product_data.append(product)
        return render(request, 'shop.html', {'products': product_data})

    def post(self, request):
        id = request.POST.get('id')
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(Q(product_id=id) & Q(user=user))
        if not shopping_cart:
            shopping_cart = ShoppingCart.objects.create(
                product_id=id,
                user_id=user
            )
            shopping_cart.save()
            messages.info(request, "Added successfully!")
            return redirect('shop')
        return redirect('/cart')


def checkout(request):
    return render(request, 'checkout.html')


class AddProductView(CreateView):
    model = Product
    template_name = 'add_product.html'
    # fields = ('name', 'price', 'description')
    form_class = ProductForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        author = request.user

        product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            author=author
        )
        product.save()
        images = request.POST.get('image')
        for image in images:
            picture = Picture.objects.create(
                image=image,
                product=product
            )
            picture.save()
        return redirect('/add_product')
