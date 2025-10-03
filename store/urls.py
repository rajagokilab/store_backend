from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),

    # Dummy payment success
    path('payment-success/<int:order_id>/', views.dummy_payment_success, name='payment_success'),
]
