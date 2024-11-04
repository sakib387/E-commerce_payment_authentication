from django.shortcuts import render
from ecommerceapp.models import Product
from math import ceil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart, Product
import requests
import logging
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
 


# Create your views here.
def index(request):
    all_products = []
    cat_prods = Product.objects.values('category', 'id')
    categories = {item['category'] for item in cat_prods}

    for category in categories:
        products = Product.objects.filter(category=category)
        n = len(products)
        slides = n // 4 + ceil((n / 4) - (n // 4))
        all_products.append({'category': category, 'products': products, 'slides': slides})

    params = {'all_products': all_products}
    return render(request, "index.html", params)

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")


 

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price for item in cart_items)
        return render(request, 'view_cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
        })
    else:
        return render(request, 'view_cart.html', {
            'cart_items': [],
            'total_price': 0,
        })


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        # Parse request data
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        try:
            # Get the product and user details
            product = Product.objects.get(id=product_id)
            user = request.user

            # Get or create a cart item for the user and product
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)

            # Increment quantity if item already exists
            if not created:
                cart_item.quantity += 1
            cart_item.save()

            # Calculate the total count and total price for the cart
            cart_items = Cart.objects.filter(user=user)
            total_count = sum(item.quantity for item in cart_items)
            total_price = sum(item.quantity * item.product.price for item in cart_items)

            return JsonResponse({
                'success': True,
                'cart_count': total_count,
                'total_price': total_price
            })

        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)

    return JsonResponse({'success': False}, status=400)





 
 

logger = logging.getLogger(__name__)

def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price for item in cart_items)
        
        # Prepare payment data with realistic values
        # views.py (Inside the checkout view)
        payment_data = {
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_passwd': settings.SSLCOMMERZ_STORE_PASS,
            'total_amount': total_price,
            'currency': 'BDT',
            'tran_id': f'TRAN_{request.user.id}_{int(total_price)}',
            'success_url': request.build_absolute_uri('/payment-success/'),
            'fail_url': request.build_absolute_uri('/payment-fail/'),
            'cancel_url': request.build_absolute_uri('/payment-cancel/'),
            'cus_name': request.user.get_full_name() or 'Customer Name',
            'cus_email': request.user.email or 'customer@example.com',
            'cus_add1': 'User Address',
            'cus_city': 'Dhaka',  # Required field for city
            'cus_country': 'Bangladesh',  # Also add country
            'cus_phone': '017XXXXXXXX',  # Replace with a valid phone number
            'shipping_method': 'NO',
            'product_name': 'Cart Items',
            'product_category': 'E-commerce',
            'product_profile': 'general',

        }


        # Send request to SSLCommerz
        url = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php' if settings.SSLCOMMERZ_SANDBOX else 'https://securepay.sslcommerz.com/gwprocess/v4/api.php'
        response = requests.post(url, data=payment_data)

        # Log and check the response
        try:
            payment_response = response.json()
            logger.info(f"SSLCommerz response: {payment_response}")
        except ValueError:
            logger.error("Failed to decode SSLCommerz response. Raw response: %s", response.text)
            messages.error(request, "Failed to initiate payment. Please try again.")
            return redirect('view_cart')

        # Print and check the response status
        print("Full Payment Response:", payment_response)
        if payment_response.get('status') == 'SUCCESS':
            return redirect(payment_response['GatewayPageURL'])
        else:
            error_message = payment_response.get('failedreason') or payment_response.get('error_message', 'Payment initialization failed.')
            print("Payment Initialization Error:", error_message)
            messages.error(request, f"Payment initialization failed: {error_message}")
            return redirect('view_cart')
    else:
        return redirect('/login/')

 
@csrf_exempt
def payment_success(request):
    if request.user.is_authenticated:
        # Check if any cart items exist for the user before attempting to delete
        cart_items = Cart.objects.filter(user=request.username)
        
        if cart_items.exists():
            print(f"Cart items before deletion: {cart_items}")
            # Clear the cart
            cart_items.delete()
            messages.success(request, 'Payment done successfully! Your cart has been cleared.')
        else:
            print("No cart items found for this user.")
            messages.info(request, 'Your cart is already empty.')
    else:
        messages.error(request, 'You need to be logged in to complete the payment.')
    
    return redirect('/')  # Redirect to homepage

@csrf_exempt
def payment_fail(request):
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('/')

@csrf_exempt
def payment_cancel(request):
    messages.warning(request, 'Payment was canceled.')
    return redirect('/')
