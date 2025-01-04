from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('product/<int:pk>/', views.product_detail, name='product'),
    path('category/<str:category_name>/', views.category_view, name='category'),
    
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    
    # New routes for favorites
    path('favorites/', views.favorite_view, name='favorite'),
    path('add-to-favorites/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:pk>/', views.remove_from_favorites, name='remove_from_favorites'),
]
