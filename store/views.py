from .models import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from . utils import *
import json
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm  
from .form import OrderForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

def store(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/store.html', context)
def cart(request):
	try:
		if request.user.is_authenticated:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer= customer, complete = False)
			items = order.orderitem_set.all()
			cartItems = order.get_cart_items
			productsstring = ''		
			for item in items:
				b = "{'imageURL': '%s','id': '%s', 'name': '%s', 'price': '%s','gettotal': '%s','quantity': '%s'}," % (item.product.imageURL,item.product.id, item.product.name, item.product.price, item.get_total, item.quantity)
				productsstring = productsstring + b
			total = order.get_cart_total
		else:
			productsstring = ''
			try:
				cart = json.loads(request.COOKIES['cart'])
			except:
				cart={}
			order = {'get_cart_total':0, 'get_cart_items':0}
			cartItems = order['get_cart_items']
			for i in cart:
				cartItems += cart[i]["quantity"]
				product = Product.objects.get(id= i)
				total = (product.price* cart[i]['quantity'])
				order['get_cart_total'] += total
				b = "{'imageURL': '%s','id': '%s', 'name': '%s', 'price': '%s','gettotal': '%s','quantity': '%s'}," % (product.imageURL,product.id, product.name, product.price, (product.price* cart[i]['quantity']),  cart[i]['quantity'])
				productsstring = productsstring + b
			total = order['get_cart_total']
	except:
		pass

	context = {'productsstring': productsstring, 'total':total, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)
def checkout(request):
	try:
		if request.user.is_authenticated:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer= customer, complete = False)
			items = order.orderitem_set.all()
			cartItems = order.get_cart_items
			productsstring = ''		
			for item in items:
				b = "{'imageURL': '%s','id': '%s', 'name': '%s', 'price': '%s','gettotal': '%s','quantity': '%s'}," % (item.product.imageURL,item.product.id, item.product.name, item.product.price, item.get_total, item.quantity)
				productsstring = productsstring + b
			total = order.get_cart_total
		else:
			productsstring = ''
			try:
				cart = json.loads(request.COOKIES['cart'])
			except:
				cart={}
			order = {'get_cart_total':0, 'get_cart_items':0}
			cartItems = order['get_cart_items']
			for i in cart:
				cartItems += cart[i]["quantity"]
				product = Product.objects.get(id= i)
				total = (product.price* cart[i]['quantity'])
				order['get_cart_total'] += total
				b = "{'imageURL': '%s','id': '%s', 'name': '%s', 'price': '%s','gettotal': '%s','quantity': '%s'}," % (product.imageURL,product.id, product.name, product.price, (product.price* cart[i]['quantity']),  cart[i]['quantity'])
				productsstring = productsstring + b
			total = order['get_cart_total']
	except:
		pass

	context = {'productsstring': productsstring, 'total':total, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)
def blog_single(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/blog_single.html', context)
def contact(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/contact_us.html', context)
def product_single(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/product_single.html', context)
def products(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/products.html', context)
def blog(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/blog.html', context)	
def about_us(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/about_us.html', context)	
def blog_details(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/blog_details.html', context)	
def logoutUser(request):
	logout(request)
	return redirect('loginPage')	
def services(request):
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/services.html', context)
def loginPage(request):
	if request.method == 'POST':
		username= request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password= password)
		if user is not None:
			login(request, user) 
			return redirect('store')
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0}
	return render(request, 'store/login.html', context)		
def register(request):
	form = CreateUserForm(request.POST)  
	if form.is_valid():
		form.save()
		username= request.POST.get('username')
		user = User.objects.get(username= username)
		login(request, user) 
		Customer.objects.create(email=user.email, user=user, name= 'macdinh')
		messages.success(request, 'Đăng ký Thành Công')
		return redirect('store')

		# return redirect('loginPage')
	products = Product.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cartItems = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cartItems = 0
		for i in cart:
			cartItems += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cartItems': cartItems, 'total':0,'form': form}		

	return render(request, 'store/register.html', context)	
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	customer = request.user.customer
	product= Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer= customer, complete = False)
	orderItem, created = OrderItem.objects.get_or_create(order= order,product= product)
	if action == 'add':
		orderItem.quantity += 1
	elif action == 'remove':
		orderItem.quantity -= 1
	orderItem.save()	
	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item added', safe= False)