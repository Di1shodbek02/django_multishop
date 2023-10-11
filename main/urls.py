from django.urls import path
from .views import HomeView, ShoppingCartView, checkout, contact, detail, IncrementCountView, DecrementCountView, \
    ShopView, AddProductView
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cart', ShoppingCartView.as_view(), name='cart'),
    path('checkout', checkout, name='checkout'),
    path('contact', contact, name='contact'),
    path('detail', detail, name='detail'),
    path('shop', ShopView.as_view(), name='shop'),
    path('increment-count', csrf_exempt(IncrementCountView.as_view()), name='increment'),
    path('decrement-count', csrf_exempt(DecrementCountView.as_view()), name='decrement'),
    path('add-product', AddProductView.as_view(), name='add_product')
]
