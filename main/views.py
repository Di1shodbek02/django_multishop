import json

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .form import ProductForm
from .models import ShoppingCart, Product, Picture
from .utls import increment_count, decrement_count


class HomeView(View):
    template_name = 'index.html'
    context = {}

    def get(self, request):
        products = Product.objects.all()[:4]
        product_data = []
        for product in products:
            image = Picture.objects.get(product=product)
            product.image = image
            product_data.append(product)

        self.context.update({'products': product_data})
        return render(request, self.template_name, self.context)

    def post(self, request):  # noqa
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
    template_name = 'shop.html'
    context = {}

    def get(self, request):
        products = Product.objects.all()
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
                user_id=user
            )
            shopping_cart.save()
            messages.info(request, "Added successfully!")
            return redirect('shop')
        return redirect('/cart')


def checkout(request):
    return render(request, 'checkout.html')


class AddProductView(View):
    form_class = ProductForm
    template_name = 'add_product.html'

    def get(self, request):
        # form = self.form_class()
        return render(request, self.template_name)

    def post(self, request):
        # form = self.form_class(request.POST, request.FILES)
        # print(form.data)

        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        description = request.POST.get('product_description')
        author = request.user  # Assuming request.user represents the product's author

        product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            user=author,
        )

        images = request.FILES.getlist('product_image')  # Correctly access the uploaded files

        for image in images:
            picture = Picture.objects.create(
                image=image,
                product=product
            )
            picture.save()
        return redirect('/')


class DetailView(View):

    def get(self, request, pk):
        products = get_object_or_404(Product, pk=pk)
        images = Picture.objects.filter(product=products).all()
        context = {
            'products': products,
            'images': images,
        }
        return render(request, 'detail.html', context)

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
            return redirect('/cart')
        return redirect('/cart')


from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from django.views import View
from .models import Product, Like


class LikeView(View):
    def post(self, request, product_id):
        user = request.user

        try:
            like = Like.objects.get(user=user, product_id=product_id)
            # Foydalanuvchi allaqachon "like" qilgan
            like.delete()
            liked = False  # Maxsulotni "like" qilishni bekor qilganligini belgilash
        except Like.DoesNotExist:
            # Foydalanuvchi maxsulotni hali "like" qilmagan
            like = Like(user=user, product_id=product_id)
            like.save()
            liked = True  # Maxsulotni "like" qilganligini belgilash

        # Maxsulotning yangi "like" san'ati
        like_count = Like.objects.filter(product_id=product_id).count()

        response_data = {
            'liked': liked,
            'like_count': like_count,
        }

        return JsonResponse(response_data)
