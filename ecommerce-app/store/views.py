from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal

from .models import Product, Category, Order, OrderItem

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST


# ===========================
# Home Page
# ===========================

def home(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get("search")

    if query:
        products = products.filter(
            name__icontains=query
        )

    return render(
        request,
        "store/home.html",
        {
            "products": products,
            "categories": categories
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

    query = request.GET.get("search")

    if query:
        products = products.filter(
            name__icontains=query
        )

    categories = Category.objects.all()

    return render(
        request,
        "store/home.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": category
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
        "store/product_detail.html",
        {
            "product": product
        }
    )


# ===========================
# Cart
# ===========================

def add_to_cart(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(pk)

    if cart.get(product_id, 0) < product.stock:
        cart[product_id] = cart.get(product_id, 0) + 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def cart(request):

    cart = request.session.get(
        "cart",
        {}
    )

    products = []
    total = Decimal("0")
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
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            }
        )

    return render(
        request,
        "store/cart.html",
        {
            "products": products,
            "total": total,
            "cart_count": cart_count
        }
    )


def increase_quantity(request, pk):

    cart = request.session.get(
        "cart",
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

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def decrease_quantity(request, pk):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(pk)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, pk):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(pk)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# ===========================
# Authentication
# ===========================

def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(request, "Please complete all required fields.")
        elif len(username) < 3:
            messages.error(request, "Username must contain at least 3 characters.")
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "This username is already registered.")
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email already exists.")
        elif len(password) < 8:
            messages.error(request, "Password must contain at least 8 characters.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Your Cartly account was created successfully.")
            return redirect("login")

    return render(request, "store/register.html")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_url = request.GET.get("next") or request.POST.get("next") or "home"
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        messages.error(request, "The username or password is incorrect.")

    return render(request, "store/login.html", {"next": next_url})


def logout_user(request):

    logout(request)

    return redirect("home")


# ===========================
# Checkout
# ===========================

@login_required(login_url="login")
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.info(request, "Your cart is empty. Add a product before checkout.")
        return redirect("cart")

    cart_items = []
    total = Decimal("0.00")
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = int(quantity)
        line_total = product.price * quantity
        cart_items.append({"product": product, "quantity": quantity, "total_price": line_total})
        total += line_total

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if not all([full_name, email, phone, address]):
            messages.error(request, "Please fill in all delivery details.")
        else:
            with transaction.atomic():
                locked_products = []
                for product_id, quantity in cart.items():
                    product = Product.objects.select_for_update().get(id=product_id)
                    quantity = int(quantity)
                    if quantity > product.stock:
                        messages.error(request, f"Only {product.stock} units of {product.name} are available.")
                        return redirect("cart")
                    locked_products.append((product, quantity))

                order = Order.objects.create(user=request.user, full_name=full_name, email=email, phone=phone, address=address)
                for product, quantity in locked_products:
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)
                    product.stock -= quantity
                    product.save(update_fields=["stock", "updated_at"])

            request.session["cart"] = {}
            request.session.modified = True
            messages.success(request, f"Order #{order.id} placed successfully.")
            return redirect("order_success", order_id=order.id)

    return render(request, "store/checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "default_name": request.user.get_full_name() or request.user.username,
        "default_email": request.user.email,
    })


# ===========================
# Orders
# ===========================

@login_required(login_url="login")
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "store/order_success.html",
        {
            "order": order
        }
    )


@login_required(login_url="login")
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(
        request,
        "store/my_orders.html",
        {
            "orders": orders
        }
    )


@login_required(login_url="login")
def order_details(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "store/order_details.html",
        {
            "order": order
        }
    )


@login_required(login_url="login")
@require_POST
def cancel_order(request, order_id):
    with transaction.atomic():
        order = get_object_or_404(
            Order.objects.select_for_update().prefetch_related("items__product"),
            id=order_id,
            user=request.user
        )

        if order.status not in {"Pending", "Processing"}:
            messages.error(request, "This order can no longer be cancelled.")
            return redirect("order_details", order_id=order.id)

        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save(update_fields=["stock", "updated_at"])

        order.status = "Cancelled"
        order.save(update_fields=["status", "updated_at"])

    messages.success(request, "Your order has been cancelled.")
    return redirect("order_details", order_id=order.id)


@login_required(login_url="login")
def order_request(request, order_id, request_type):
    if request_type not in {"Return", "Exchange"}:
        return redirect("my_orders")

    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != "Delivered":
        messages.error(request, f"{request_type} requests are available after delivery.")
        return redirect("order_details", order_id=order.id)

    if request.method == "POST":
        from .models import OrderRequest

        item = get_object_or_404(OrderItem, id=request.POST.get("item_id"), order=order)
        existing_request = order.order_requests.filter(
            order_item=item,
            request_type=request_type,
            status__in=["Requested", "Approved"]
        ).exists()

        if existing_request:
            messages.error(request, f"A {request_type.lower()} request already exists for this item.")
        elif not request.POST.get("reason"):
            messages.error(request, "Please select a reason for your request.")
        else:
            OrderRequest.objects.create(
                order=order,
                order_item=item,
                user=request.user,
                request_type=request_type,
                reason=request.POST["reason"],
                details=request.POST.get("details", "")
            )
            messages.success(request, f"Your {request_type.lower()} request was submitted.")
            return redirect("order_details", order_id=order.id)

    return render(
        request,
        "store/order_request.html",
        {"order": order, "request_type": request_type}
    )


# ===========================
# Forgot Password
# ===========================

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get(
            "email"
        )

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
        "store/forgot_password.html"
    )

