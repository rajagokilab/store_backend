from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import uuid

from .models import Category, Product, Order, OrderItem

# ------------------------
# Home Page
# ------------------------
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'store/home.html', {'categories': categories, 'products': products})

# ------------------------
# Add Item to Cart
# ------------------------
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')  # redirect to cart page

# ------------------------
# View Cart
# ------------------------
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=int(pid))
        total_price = product.price * qty
        items.append({'product': product, 'quantity': qty, 'total_price': total_price})
        total += total_price
    return render(request, 'store/cart.html', {'items': items, 'total': total})

# ------------------------
# Checkout Page (Dummy Payment)
# ------------------------
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')

    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=int(pid))
        total_price = product.price * qty
        items.append({'product': product, 'quantity': qty, 'total_price': total_price})
        total += total_price

    # Save total in session
    request.session['total_amount'] = total

    # Create dummy order (Pending)
    order = Order.objects.create(total_amount=total, payment_status="Pending")
    for item in items:
        OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])

    # Pass items and total to template
    return render(request, 'store/checkout.html', {
        'items': items,
        'total': total,
        'order': order
    })
def dummy_payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Mark as paid
    order.payment_status = "Success"
    order.save()
    
    # Clear cart
    request.session['cart'] = {}
    request.session['total_amount'] = 0

    # Redirect to invoice
    return redirect('download_invoice', order_id=order.id)



# ------------------------
# Dummy Payment Success
# ------------------------
def payment_success(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.payment_status = "Success"
        order.save()
        # Clear cart
        request.session['cart'] = {}
        request.session['total_amount'] = 0
        return redirect('download_invoice', order_id=order.id)

# ------------------------
# Download Invoice PDF
# ------------------------
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, f"GST Invoice for Order #{order_id}")

    y = 750
    p.setFont("Helvetica", 12)
    for item in order.orderitem_set.all():
        p.drawString(100, y, f"{item.product.name} x {item.quantity} = ₹{item.product.price * item.quantity}")
        y -= 25

    p.drawString(100, y - 20, f"Total: ₹{order.total_amount}")
    p.showPage()
    p.save()
    return response
