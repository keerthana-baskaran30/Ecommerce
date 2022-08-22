from django import urls
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("ecommerce/login", views.LoginView.as_view()),
    path("ecommerce/customer/register", views.UserRegisterView.as_view()),
    path("ecommerce/product/", views.ListProducts.as_view()),
    path("ecommerce/product/pid/", views.DetailProducts.as_view()),
    path("ecommerce/product/category/", views.DetailCategory.as_view()),
    path("ecommerce/cart/add", views.CartAddView.as_view()),
    path("ecommerce/cartitems/", views.DetailCart.as_view()),
    path("ecommerce/cartitems/delete", views.DeleteCartView.as_view()),
    path("ecommerce/seller/product/add", views.SellerAddView.as_view()),
    path("ecommerce/seller/product/delete", views.SellerDeleteView.as_view()),
    path("ecommerce/seller/product", views.SellerDisplayView.as_view()),
    path("ecommerce/seller/register", views.SellerRegisterView.as_view()),
    path("ecommerce/seller/product/update", views.SellerUpdateView.as_view()),
]
