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
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def shipped(request, pk):
	order1 = Order.objects.get(id= pk)
	order1.shipped = True
	order1.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))	
@user_passes_test(lambda u: u.is_superuser)
def address_info(request,pk):
	order1 = Order.objects.get(id= pk)
	categories = Category.objects.order_by("id")[:10]
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'cart_quantity': cart_quantity, 'total':0, 'order1': order1}
	return render(request, 'store/address_info.html', context)
@user_passes_test(lambda u: u.is_superuser)
def orders(request):
	orders = Order.objects.filter(complete = True,shipped = False).order_by("id")
	categories = Category.objects.order_by("id")[:10]

	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'cart_quantity': cart_quantity, 'total':0, 'orders': orders}
	return render(request, 'store/orders.html', context)

def payment(request):
	import urllib.request
	import urllib
	import uuid
	import requests
	import hmac
	import hashlib
	if request.method == 'POST': 
		price =  request.POST.get('price') 
		name =  request.POST.get('name')
		address =  request.POST.get('address') 
		email =  request.POST.get('email') 
		city =  request.POST.get('price') 
		phone =  request.POST.get('phone') 
		if name and address and email and city and phone:
			pass
		else:
			messages.success(request, 'Vui lòng điền đầy đủ thông tin')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		order_id = int(request.POST.get('order_id'))

		if (order_id < 0) : 

			order = Order.objects.create( complete = True)
			try:
				cart = json.loads(request.COOKIES['cart'])
			except:
				cart={}
			for i in cart:
				product = Product.objects.get(id= i)
				orderItem = OrderItem.objects.create(product=product,order=order, quantity=cart[i]['quantity'] )
		else:
			order = Order.objects.get(id=order_id)
			order.complete = True
			order.save()

		Address.objects.create(name= name, address= address, city=city,phone = phone,order = order)
		price = str(int(price)*1000)
		# parameters send to MoMo get get payUrl
		endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
		partnerCode = "MOMO"
		accessKey = "F8BBA842ECF85"
		secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
		orderInfo = "pay with MoMo"
		redirectUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
		ipnUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
		amount = price
		orderId = str(uuid.uuid4())
		requestId = str(uuid.uuid4())
		requestType = "captureWallet"
		extraData = ""  # pass empty value or Encode base64 JsonString

		# before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
		# &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
		# &requestType=$requestType
		rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType

		# puts raw signature
		print("--------------------RAW SIGNATURE----------------")
		print(rawSignature)
		# signature
		h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
		signature = h.hexdigest()
		print("--------------------SIGNATURE----------------")
		print(signature)

		# json object send to MoMo endpoint

		data = {
			'partnerCode': partnerCode,
			'partnerName': "Test",
			'storeId': "MomoTestStore",
			'requestId': requestId,
			'amount': amount,
			'orderId': orderId,
			'orderInfo': orderInfo,
			'redirectUrl': redirectUrl,
			'ipnUrl': ipnUrl,
			'lang': "vi",
			'extraData': extraData,
			'requestType': requestType,
			'signature': signature
		}
		print("--------------------JSON REQUEST----------------\n")
		data = json.dumps(data)
		print(data)

		clen = len(data)
		response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

		# f.close()
		print("--------------------JSON response----------------\n")
		print(response.json())
		print( price)
		# print(response.json()['payUrl'])
		return redirect(response.json()['payUrl'])
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def feedback(request):
	if request.method == 'POST':
		name= request.POST.get('name')
		email= request.POST.get('email')
		comment =request.POST.get('comment')
		Feedback.objects.create( name= name, email = email, comment = comment)
		messages.success(request, 'Gửi tin thành công')
	return redirect('contact')	
def review_stars(request, stars, pk):
	product = Product.objects.get(id=pk)
	review, created = Review.objects.get_or_create(user= request.user,product= product)

	if(review.first_time):
		review.first_time = False
		product.stars = ((product.stars*product.review_times + stars)/(product.review_times+1))
		product.review_times += 1
	else:
		product.stars = ((product.stars*product.review_times + stars - review.stars)/(product.review_times))
	review.b = round(review.stars, 0)
	review.stars = stars
	product.save()
	review.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))	
def blog_details(request, pk):

	products = Product.objects.order_by("id")[:7]
	categories = Category.objects.order_by("id")[:10]
	blogs = Blog.objects.order_by("id")[:4]
	blog = Blog.objects.get(id=pk)
	# tag = get_object_or_404(Tag, slug=tag_slug)

	if request.method == 'POST':
		description = request.POST.get('comment')
		Blog_comment.objects.create( user=request.user, description = description, blog = blog)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products,'categories':categories, 'cart_quantity': cart_quantity, 'total':0, 'blog': blog, 'blogs':blogs}
	return render(request, 'store/blog_details.html', context)	


def logoutUser(request):
	logout(request)
	return redirect('loginPage')	

def loginPage(request):
	categories = Category.objects.order_by("id")[:10]
	if request.method == 'POST':
		username= request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password= password)
		if user is not None:
			login(request, user) 
			return redirect('store')
		messages.success(request, 'Tài khoản hoặc mật khẩu không chính xác')
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0}
	return render(request, 'store/login.html', context)		
def register(request):
	form = CreateUserForm(request.POST or None)  
	if form.is_valid():
		form.save()
		username= request.POST.get('username')
		user = User.objects.get(username= username)
		login(request, user) 
		Customer.objects.create(email=user.email, user=user, name= user.username)
		messages.success(request, 'Đăng ký Thành Công')
		return redirect('store')

		# return redirect('loginPage')
	categories = Category.objects.order_by("id")[:10]
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0,'form': form}		

	return render(request, 'store/register.html', context)	

def single_product(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == 'POST':
		description = request.POST.get('comment')
		Comment.objects.create( user=request.user, description = description, product = product)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	products = Product.objects.order_by("id")[:7]
	categories = Category.objects.order_by("id")[:10]

	if request.user.is_authenticated:
		review, created = Review.objects.get_or_create(user= request.user,product= product)
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:	
		review = 0	
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products,'categories':categories, 'cart_quantity': cart_quantity, 'total':0, 'product': product, 'review':review}
	return render(request, 'store/single-product.html', context)	

def category(request, pk):
	category = Category.objects.get(id=pk)
	categories = Category.objects.all()
	
	if request.user.is_authenticated:

		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:	
		review = 0	
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0, 'category': category}
	return render(request, 'store/products.html', context)
def search(request):

	categories = Category.objects.all()
	if request.method == 'GET':   
		q =  request.GET.get('q')     

		products= Product.objects.filter(name__contains=q)
	else:
		products =Product.objects.all()
	if request.user.is_authenticated:

		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:	
		review = 0	
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0,'products':products, 'q': q}
	return render(request, 'store/products.html', context)

def store(request):
	products = Product.objects.order_by("id")[:7]
	products1 = Product.objects.order_by("-review_times")[:7]
	categories = Category.objects.order_by("id")[:10]
	blogs = Blog.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products,'products1': products1,'categories':categories, 'cart_quantity': cart_quantity, 'total':0, 'blogs': blogs}
	return render(request, 'store/store.html', context)
def cart(request):
	categories = Category.objects.order_by("id")[:10]
	try:
		if request.user.is_authenticated:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer= customer, complete = False)
			items = order.orderitem_set.all()
			cart_quantity = order.get_cart_items
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
			cart_quantity = order['get_cart_items']
			for i in cart:
				cart_quantity += cart[i]["quantity"]
				product = Product.objects.get(id= i)
				total = (product.price* cart[i]['quantity'])
				order['get_cart_total'] += total
				b = "{'imageURL': '%s','id': '%s', 'name': '%s', 'price': '%s','gettotal': '%s','quantity': '%s'}," % (product.imageURL,product.id, product.name, product.price, (product.price* cart[i]['quantity']),  cart[i]['quantity'])
				productsstring = productsstring + b
			total = order['get_cart_total']
	except:
		pass

	context = {'productsstring': productsstring,'categories':categories, 'total':total, 'cart_quantity': cart_quantity}
	return render(request, 'store/cart.html', context)
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
def checkout(request):
	categories = Category.objects.order_by("id")[:10]
	try:
		if request.user.is_authenticated:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer= customer, complete = False)
			order_id = order.id
			items = order.orderitem_set.all()
			cart_quantity = order.get_cart_items
		
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
			cart_quantity = order['get_cart_items']
			for i in cart:
				cart_quantity += cart[i]["quantity"]
				product = Product.objects.get(id= i)
				total = (product.price* cart[i]['quantity'])
				order['get_cart_total'] += total
				b = "{'imageURL': '%s','id': '%s', 'name': '%s', 'price': '%s','gettotal': '%s','quantity': '%s'}," % (product.imageURL,product.id, product.name, product.price, (product.price* cart[i]['quantity']),  cart[i]['quantity'])
				productsstring = productsstring + b
			total = order['get_cart_total']
			order_id = -1
	except:
		pass

	context = {'productsstring': productsstring,'categories':categories, 'total':total, 'cart_quantity': cart_quantity, 'order_id': order_id}
	return render(request, 'store/checkout.html', context)

def contact(request):
	categories = Category.objects.order_by("id")[:10]
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0}
	return render(request, 'store/contact_us.html', context)

def products(request):
	products = Product.objects.all()
	categories = Category.objects.all()
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'products': products, 'cart_quantity': cart_quantity, 'categories': categories, 'total':0}
	return render(request, 'store/products.html', context)
def blog(request):
	blogs = Blog.objects.all()
	categories = Category.objects.order_by("id")[:10]

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'blogs': blogs,'categories':categories, 'cart_quantity': cart_quantity, 'total':0}
	return render(request, 'store/blog.html', context)	
def about_us(request):
	categories = Category.objects.order_by("id")[:10]
	# try:
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		cart_quantity = order.get_cart_items
	else:		
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		cart_quantity = 0
		for i in cart:
			cart_quantity += cart[i]["quantity"]
	# except:
	# 	pass
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0}
	return render(request, 'store/about_us.html', context)	














