from django.urls import path

from . import views



urlpatterns = [

    # Home
    path(
        '',
        views.home,
        name='home'
    ),



    # Category
    path(
        'category/<int:category_id>/',
        views.category_products,
        name='category_products'
    ),



    # Product Details
    path(
        'product/<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),



    # Cart
    path(
        'cart/',
        views.cart,
        name='cart'
    ),



    path(
        'cart/add/<int:pk>/',
        views.add_to_cart,
        name='add_to_cart'
    ),



    path(
        'cart/increase/<int:pk>/',
        views.increase_quantity,
        name='increase_quantity'
    ),



    path(
        'cart/decrease/<int:pk>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),



    path(
        'cart/remove/<int:pk>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),



    # Authentication
    path(
        'register/',
        views.register,
        name='register'
    ),


    path(
        'login/',
        views.login_user,
        name='login'
    ),


    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),



    # Checkout
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),


    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),



    # Orders
    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),


    path(
        'order-details/<int:order_id>/',
        views.order_details,
        name='order_details'
    ),



    # Forgot Password
    path(
        'forgot-password/',
        views.forgot_password,
        name='forgot_password'
    ),

]