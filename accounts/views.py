from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Category, Customer, Product, Order, Cart, CartItem

# Home page
def home(request):
    query = request.GET.get('search', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'index.html', {'products': products, 'query': query})

# Login page
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'signup.html', {'section': 'login'})

# Register page
def user_register(request):
    if request.method == "POST":
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Customer.objects.create(user=user)
            messages.success(request, "Account created successfully!")
            return redirect('login')
    return render(request, 'signup.html', {'section': 'register'})

# Logout page
def logout_view(request):
    logout(request)
    return redirect('home')

# Product detail page
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})

# Category page
def category_view(request, category_name):
    category_name = category_name.replace('-', ' ')
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'products': products, 'category': category})

# Cart page
def cart_view(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
        items = CartItem.objects.filter(cart=cart)
        
        subtotal = sum(item.product.sale_price * item.quantity if item.product.sale_price else item.product.price * item.quantity for item in items)
        shipping = 10  # You can adjust this logic based on shipping rules
        total = subtotal + shipping

        return render(request, 'cart.html', {'items': items, 'subtotal': subtotal, 'shipping': shipping, 'total': total})
    else:
        messages.error(request, "You need to login to view the cart.")
        return redirect('login')

# Add to cart page
def add_to_cart(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        customer = get_object_or_404(Customer, user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        
        messages.success(request, f"{product.name} added to cart.")
        return redirect('cart')
    else:
        messages.error(request, "You need to login to add items to the cart.")
        return redirect('login')

# Remove from cart page
def remove_from_cart(request, pk):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
        return redirect('cart')
    else:
        messages.error(request, "You need to login to remove items from the cart.")
        return redirect('login')

# Update cart item quantity
def update_cart_item(request, pk):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, pk=pk)
        quantity = request.POST.get('quantity')
        
        if quantity:
            quantity = int(quantity)
            if quantity > 10:
                messages.error(request, "You cannot add more than 10 items.")
                return redirect('cart')
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart item updated.")
        
        return redirect('cart')
    else:
        messages.error(request, "You need to login to update items in the cart.")
        return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Customer, Product, Favorite, Cart, CartItem

# Favorite page
def favorite_view(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
        favorites = Favorite.objects.filter(customer=customer)
        return render(request, 'favorites.html', {'favorites': favorites})
    else:
        messages.error(request, "You need to login to view your favorites.")
        return redirect('login')

# Add to favorites page
def add_to_favorites(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        customer = get_object_or_404(Customer, user=request.user)
        
        # Check if the product is already in the favorites list
        if Favorite.objects.filter(customer=customer, product=product).exists():
            messages.info(request, f"{product.name} is already in your favorites.")
        else:
            Favorite.objects.create(customer=customer, product=product)
            messages.success(request, f"{product.name} added to favorites.")
        
        return redirect('favorite')
    else:
        messages.error(request, "You need to login to add items to your favorites.")
        return redirect('login')

# Remove from favorites page
def remove_from_favorites(request, pk):
    if request.user.is_authenticated:
        favorite = get_object_or_404(Favorite, pk=pk)
        favorite.delete()
        messages.success(request, "Item removed from favorites.")
        return redirect('favorite')
    else:
        messages.error(request, "You need to login to remove items from your favorites.")
        return redirect('login')
