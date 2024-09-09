from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

# Отображение всех товаров
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Добавление товара в корзину
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart_detail')

# Удаление товара из корзины
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart_detail')

# Отображение содержимого корзины
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    total_sum = sum(item['total_price'] for item in cart_items)

    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total_sum': total_sum})
