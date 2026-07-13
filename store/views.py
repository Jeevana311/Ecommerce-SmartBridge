from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal

from .models import Product, Category, Order, OrderItem

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages




# ===========================
# Home Page
# ===========================

def home(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    query = request.GET.get('search')


    if query:

        products = products.filter(
            name__icontains=query
        )


    return render(
        request,
        'store/home.html',
        {
            'products': products,
            'categories': categories
        }
    )




# ===========================
# Category Products
# ===========================

def category_products(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )


    products = Product.objects.filter(
        category=category
    )


    categories = Category.objects.all()


    return render(
        request,
        'store/home.html',
        {
            'products': products,
            'categories': categories,
            'selected_category': category
        }
    )




# ===========================
# Product Details
# ===========================

def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )


    return render(
        request,
        'store/product_detail.html',
        {
            'product': product
        }
    )




# ===========================
# Add To Cart
# ===========================

def add_to_cart(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )


    cart = request.session.get(
        'cart',
        {}
    )


    product_id = str(pk)


    quantity = cart.get(
        product_id,
        0
    )


    if quantity < product.stock:

        cart[product_id] = quantity + 1



    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')





# ===========================
# Cart
# ===========================

def cart(request):

    cart = request.session.get(
        'cart',
        {}
    )


    products = []

    total = Decimal('0')

    cart_count = 0



    for product_id, quantity in cart.items():


        product = get_object_or_404(
            Product,
            id=product_id
        )


        subtotal = product.price * quantity


        total += subtotal

        cart_count += quantity



        products.append(
            {
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            }
        )



    return render(
        request,
        'store/cart.html',
        {
            'products': products,
            'total': total,
            'cart_count': cart_count
        }
    )





# ===========================
# Increase Quantity
# ===========================

def increase_quantity(request, pk):

    cart = request.session.get(
        'cart',
        {}
    )


    product = get_object_or_404(
        Product,
        id=pk
    )


    product_id = str(pk)



    if product_id in cart:

        if cart[product_id] < product.stock:

            cart[product_id] += 1



    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')





# ===========================
# Decrease Quantity
# ===========================

def decrease_quantity(request, pk):

    cart = request.session.get(
        'cart',
        {}
    )


    product_id = str(pk)



    if product_id in cart:


        cart[product_id] -= 1



        if cart[product_id] <= 0:

            del cart[product_id]



    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')





# ===========================
# Remove Cart
# ===========================

def remove_from_cart(request, pk):

    cart = request.session.get(
        'cart',
        {}
    )


    product_id = str(pk)



    if product_id in cart:

        del cart[product_id]



    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')





# ===========================
# Register
# ===========================

def register(request):


    if request.method == "POST":


        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')



        if User.objects.filter(
            username=username
        ).exists():


            messages.error(
                request,
                "Username already exists"
            )


            return redirect('register')




        if User.objects.filter(
            email=email
        ).exists():


            messages.error(
                request,
                "Email already registered"
            )


            return redirect('register')




        User.objects.create_user(

            username=username,

            email=email,

            password=password

        )



        messages.success(
            request,
            "Registration successful"
        )


        return redirect('login')



    return render(
        request,
        'store/register.html'
    )





# ===========================
# Login
# ===========================

def login_user(request):


    if request.method == "POST":


        username = request.POST.get('username')

        password = request.POST.get('password')



        user = authenticate(

            username=username,

            password=password

        )



        if user:


            login(
                request,
                user
            )


            return redirect('home')



        else:


            messages.error(
                request,
                "Invalid username or password"
            )



    return render(
        request,
        'store/login.html'
    )





# ===========================
# Logout
# ===========================

def logout_user(request):

    logout(request)

    return redirect('home')





# ===========================
# Checkout
# ===========================

@login_required(login_url='login')
def checkout(request):


    cart = request.session.get(
        'cart',
        {}
    )


    if not cart:

        return redirect('cart')



    if request.method == "POST":



        order = Order.objects.create(

            user=request.user,

            full_name=request.POST.get('full_name'),

            email=request.POST.get('email'),

            phone=request.POST.get('phone'),

            address=request.POST.get('address')

        )




        for product_id, quantity in cart.items():



            product = get_object_or_404(
                Product,
                id=product_id
            )



            if product.stock >= quantity:



                OrderItem.objects.create(

                    order=order,

                    product=product,

                    quantity=quantity

                )



                product.stock -= quantity

                product.save()




        request.session['cart'] = {}

        request.session.modified = True




        return redirect(
            'order_success',
            order.id
        )




    return render(
        request,
        'store/checkout.html'
    )





# ===========================
# Order Success
# ===========================

@login_required(login_url='login')
def order_success(request, order_id):


    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user

    )



    return render(

        request,

        'store/order_success.html',

        {
            'order':order
        }

    )





# ===========================
# My Orders
# ===========================

@login_required(login_url='login')
def my_orders(request):


    orders = Order.objects.filter(

        user=request.user

    ).order_by('-id')



    return render(

        request,

        'store/my_orders.html',

        {
            'orders':orders
        }

    )





# ===========================
# Order Details
# ===========================

@login_required(login_url='login')
def order_details(request, order_id):


    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user

    )



    return render(

        request,

        'store/order_details.html',

        {
            'order':order
        }

    )





# ===========================
# Forgot Password
# ===========================

def forgot_password(request):


    if request.method == "POST":


        email = request.POST.get('email')



        user = User.objects.filter(
            email=email
        ).first()



        if user:


            messages.success(
                request,
                "Password reset instructions sent"
            )


        else:


            messages.error(
                request,
                "Email not registered"
            )



    return render(

        request,

        'store/forgot_password.html'

    )