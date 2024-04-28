from django.shortcuts import render, redirect
from .models import *
from .utils import *
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
import datetime
from rest_framework.decorators import api_view

# Create your views here
def profile(request):
    data = cartData(request)
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer, complete=True, approved=True)
    order_items = [item for order in orders for item in order.orderitem_set.all()]
    order = data['order'] 
    # statuses = Status.objects.all()
    statuses = Status.objects.filter(order__in=orders)
    context = {'orders': orders, 'order_items': order_items, 'order':order,'statuses': statuses}
    return render(request, 'profile.html', context)

def chef_panel(request):
    orders = Order.objects.filter(customer=request.user.customer, complete=True, approved=True)
    status_choices = [(choice, label) for choice, label in Status.ORDER_STATUS_CHOICES]
    time_choices = [(choice, label) for choice, label in Status.TIME_CHOICES]
    order_items = [item for order in orders for item in order.orderitem_set.all()]
    context = {'orders': orders, 'status_choices': status_choices, 'time_choices': time_choices, 'order_items': order_items}
    return render(request, 'chef_panel.html', context)

def update_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        time_needed = int(request.POST.get('time_needed'))

        # Get the current user's orders
        orders = Order.objects.filter(customer=request.user.customer, complete=True, approved=True)

        # Update or create a Status object for each order
        for order in orders:
            status_obj, created = Status.objects.get_or_create(order=order)
            status_obj.status = status
            status_obj.time_needed = time_needed
            status_obj.save()

        return redirect('chef_panel')

    return redirect('chef_panel')

def home(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    products = data['items']

    products = Menu.objects.all()
    context = {'products':products, 'order':order, 'cartItems':cartItems}
    print("products =",products)
    print("orders =",order)
    print("products =",cartItems)
    return render(request, 'home.html',context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)

def logout(request):
      auth_logout(request)
      return redirect('login')
      
@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('login')
        else:
            form.add_error(None, "username already taken")
    else:
        form = CustomerForm()
    return render(request,'register.html', {'form': form})

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	# print('Action:', action)
	# print('Product:', productId)

	customer = request.user.customer
	product = Menu.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def checkout(request):
	return render(request, 'payment.html')

def payment(request):
	transaction_id = datetime.datetime.now().timestamp()
	# data = json.loads(request.body)


	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	# total = float(data['form']['total'])
	total = True
	order.transaction_id = transaction_id

	# if total == order.get_cart_total:
	# 	order.complete = True
	# order.save()
 
	if total == True:
		order.complete = True
	order.save()

	# if order.approved == True:
	# 	chef, created = Chef.objects.get_or_create(order=order, time_needed=5, status="preparing")
    
	# 	chef.save()

	chef, created = Status.objects.get_or_create(order=order, time_needed=5, status="preparing")

	chef.save()

	# return JsonResponse('Payment submitted..', safe=False)
	return redirect('home')


 

	