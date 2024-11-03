from django.shortcuts import render
from ecommerceapp.models import Product
from math import ceil

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