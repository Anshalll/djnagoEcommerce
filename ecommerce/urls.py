from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name="index"),
    path('cart/', views.cart, name="cart"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("register/", views.register, name="register"),
    path("tracking/", views.tracking, name="tracking"),
    path("categories/", views.categories, name="categories"),
    path("contact/", views.contact, name="contact"),
    path("productview/<int:slug>/", views.productview, name="productview"),
    path("products/<str:slug>/", views.products, name="products"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("addtocart/<int:slug>/", views.addtocart, name = "addtocart"),
    path("cartupdateadd/<int:slug>/" , views.cartupdateadd, name="cartupdateadd"),
    path("cartdel/<int:slug>/", views.cartdel, name="cartdel"),
    path("cartupdateremove/<int:slug>/", views.cartupdateremove, name="cartupdateremove"),
    path("info/", views.info, name="info"),
    path('payment/', views.payment, name="payment"),
    path('orders/', views.orders, name="orders"),
    path('userorders/', views.userorders, name="userorders"),



]
