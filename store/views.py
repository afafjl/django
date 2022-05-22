from .models import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from . utils import *
import json
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm  
from .form import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser) #chỉ cho phép admin truy cập
def shipped(request, pk):
	"""
	hàm đổi trạng thái sau khi đơn hàng hoàn tất, 
	input là id của order, request
	sau đó trả lại về đường dẫn cũ
	"""
	order1 = Order.objects.get(id= pk)
	order1.shipped = True
	order1.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))	

@user_passes_test(lambda u: u.is_superuser)#chỉ cho phép admin truy cập
def address_info(request,pk):
	"""
	hàm đưa ra trang thông tin của đơn hàng 
	input là id order , request
	render ra trang address_info với output là order đó và thông tin liên trên nav 
	"""	
	order1 = Order.objects.get(id= pk)
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'cart_quantity': cart_quantity, 'total':0, 'order1': order1}
	return render(request, 'store/address_info.html', context)

@user_passes_test(lambda u: u.is_superuser)#chỉ cho phép admin truy cập
def orders(request):
	"""	
	hàm đưa ra trang chứa tất cả các order đã được đặt mà chưa được giao hàng
	render trang orders với output là thông tin trên nav và các order trên
	"""
	orders = Order.objects.filter(complete = True,shipped = False).order_by("id")
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'cart_quantity': cart_quantity, 'total':0, 'orders': orders}
	return render(request, 'store/orders.html', context)


def cart(request):
	"""
	hàm xuất dữ liệu ra trang giỏ hàng 
	dữ liệu trong giỏ hàng được trả về dạng chuỗi
	render trang cart với các thông tin về giỏ hàng, và các category
	"""
	categories = Category.objects.order_by("id")[:10]
	productsstring, total, cart_quantity = cartdata(request)#gọi hàm cartdata từ file utils.py
	context = {'productsstring': productsstring,'categories':categories, 'total':total, 'cart_quantity': cart_quantity}
	return render(request, 'store/cart.html', context)

def checkout(request):
	"""
	hàm xuất dữ liệu ra trang checkout
	dữ liệu trong giỏ hàng được trả về dạng chuỗi
	render trang cart với các thông tin về giỏ hàng,id của order và các category
	"""	
	categories = Category.objects.order_by("id")[:10]
	productsstring, total, cart_quantity = cartdata(request)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete = False)
		order_id = order.id
	else:
		order_id = -1
	context = {'productsstring': productsstring,'categories':categories, 'total':total, 'cart_quantity': cart_quantity, 'order_id': order_id}
	return render(request, 'store/checkout.html', context)

def payment(request):
	"""
	hàm xứ lý thanh toán qua momo, lưu thông tin order
	input la dữ liệu ng dùng qua phương thưc post
	"""
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
		#lưu thông tin đơn hàng
		order = saveOrder(request, order_id)#gọi hàm saveOrder bên utils.py
		Address.objects.create(name= name, address= address, city=city,phone = phone,order = order)
		#chuyển thông tin sang bên môi trường momo test
		return redirect(momo(request, price))#gọi hàm momo bên utils.py
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def feedback(request):
	"""
	hàm lưu thông tin về các feedback của người dùng
	input là thông tin feedback qua phương thức POST
	sau đó redirect về trang contact với message
	"""
	if request.method == 'POST':
		name= request.POST.get('name')
		email= request.POST.get('email')
		comment =request.POST.get('comment')
		Feedback.objects.create( name= name, email = email, comment = comment)
		messages.success(request, 'Gửi tin thành công')
	return redirect('contact')	

def products(request):

	"""
	hàm xuất dữ liệu ra trang products
	render ra trang products với thông tin về giỏ hàng, tất cả sản phẩm và các danh mục
	"""
	products = Product.objects.all()
	categories = Category.objects.all()
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'products': products, 'cart_quantity': cart_quantity, 'categories': categories, 'total':0}
	return render(request, 'store/products.html', context)

def single_product(request, pk):
	"""
	hàm xuất dữ liệu ra trang thông tin chi tiết sản phẩm và xử lý nếu người dùng có bình luận
	input là id sản phẩm, request, thông tin bình luận nếu có
	render ra trang single-product với thông tin về các sản phẩm, sản phẩm này, thông tin giỏ hàng, đỉểm review
	"""
	product = Product.objects.get(id=pk)
	if request.method == 'POST':#nếu người dùng có bình luận 
		description = request.POST.get('comment')
		Comment.objects.create( user=request.user, description = description, product = product)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	products = Product.objects.order_by("id")[:7]
	categories = Category.objects.order_by("id")[:10]

	if request.user.is_authenticated:#nếu người dùng đã đăng nhập thì khởi tạo dữ liêu review mới cho database
		review, created = Review.objects.get_or_create(user= request.user,product= product)
	else:
		review = 0
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'products': products,'categories':categories, 'cart_quantity': cart_quantity, 'total':0, 'product': product, 'review':review}
	return render(request, 'store/single-product.html', context)	

def review_stars(request, stars, pk):
	"""
	hàm lưu điểm đánh giá sản phẩm
	input là gồm điểm đánh giá và id của sản phẩm, request
	sau đó return về trang cũ
	"""
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

def blog(request):
	"""
	hàm xuất dữ liệu ra trang blog
	render ra trang blog với thông tin về giỏ hàng, tất cả blog và các danh mục
	"""
	blogs = Blog.objects.all()
	categories = Category.objects.order_by("id")[:10]

	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'blogs': blogs,'categories':categories, 'cart_quantity': cart_quantity, 'total':0}
	return render(request, 'store/blog.html', context)	

def blog_details(request, pk):
	"""
	hàm xuất dữ liệu ra trang thông tin chi tiết bài viết
	input là id của blog và request, bình luận nếu có
	render ra trang blog_detail với các thông tin liên quan như các sản phẩm, danh mục, thanh nav, blog này, blog liên quan
	"""
	products = Product.objects.order_by("id")[:7]
	categories = Category.objects.order_by("id")[:10]
	blogs = Blog.objects.order_by("id")[:4]
	blog = Blog.objects.get(id=pk)
	# tag = get_object_or_404(Tag, slug=tag_slug)
	#nếu người dùng có bình luận vào bài viết này
	if request.method == 'POST':
		description = request.POST.get('comment')
		Blog_comment.objects.create( user=request.user, description = description, blog = blog)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'products': products,'categories':categories, 'cart_quantity': cart_quantity, 'total':0, 'blog': blog, 'blogs':blogs}
	return render(request, 'store/blog_details.html', context)	

def logoutUser(request):
	"""	hàm dùng để đăng xuất"""
	logout(request)
	return redirect('loginPage')	

def loginPage(request):
	"""	
	hàm dùng để tạo đăng nhập
	nếu đăng nhập thành công sẽ được chuyển tới trang store với message thành công
	nếu không thành công sẽ trở lại trang login với message tk mk kông chính xác
	"""
	categories = Category.objects.order_by("id")[:10]
	if request.method == 'POST':
		username= request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password= password)
		if user is not None:
			login(request, user) 
			return redirect('store')
		messages.success(request, 'Tài khoản hoặc mật khẩu không chính xác')
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0}
	return render(request, 'store/login.html', context)		

def register(request):
	"""
	hàm dùng để tạo đăng ký
	nếu đăng nhập thành công sẽ được chuyển tới trang store với message thành công
	nếu không thành công sẽ trở lại trang register với message liên quan
	"""
	form = CreateUserForm(request.POST or None)#gọi class CreateUserForm từ form.py  
	if form.is_valid():
		form.save()
		username= request.POST.get('username')
		user = User.objects.get(username= username)
		login(request, user)
		Customer.objects.create(email=user.email, user=user, name= user.username)
		messages.success(request, 'Đăng ký Thành Công')
		return redirect('store')

	categories = Category.objects.order_by("id")[:10]
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0,'form': form}		

	return render(request, 'store/register.html', context)	

def category(request, pk):
	"""
	hàm xuất dữ liệu ra trang sản phẩm lọc theo category
	input là id của category
	render ra trang products với thông tin về category, các category khác, thông tin giỏ hàng
	"""
	category = Category.objects.get(id=pk)
	categories = Category.objects.all()	
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0, 'category': category}
	return render(request, 'store/products.html', context)

def search(request):
	"""
	hàm tìm kiếm sản phẩm
	input là từ tìm kiếm với phương thức GET
	render ra trang products với thông tin về sản phẩm chứa từ khóa tìm kiếm, các category, thông tin giỏ hàng
	"""
	categories = Category.objects.all()
	if request.method == 'GET':   
		q =  request.GET.get('q')     

		products= Product.objects.filter(name__icontains=q)
	else:
		products =Product.objects.all()
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0,'products':products, 'q': q}
	return render(request, 'store/products.html', context)

def store(request):
	"""
	hàm xuất dữ liệu ra trang chính
	render ra trang store với các thông tin về các sản phẩm mới, sản phẩm nổi bật, thông tin giỏ hàng, và các bài viết mới
	"""
	products = Product.objects.order_by("id")[:7]
	products1 = Product.objects.order_by("-review_times")[:7]
	categories = Category.objects.order_by("id")[:10]
	blogs = Blog.objects.all()
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'products': products,'products1': products1,'categories':categories, 'cart_quantity': cart_quantity, 'total':0, 'blogs': blogs}
	return render(request, 'store/store.html', context)

#hàm xử lý logic khi người dùng thêm hay xóa sản phẩm trong giỏ hàng
def updateItem(request):
	"""
	hàm xử lý khi tăng giảm số lượng sản phẩm trong giỏ hàng
	input là id của sản phẩm, request và phương thức tăng giảm
	trả về message là item added
	"""
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

def contact(request):
	"""
	hàm xuất dữ liệu ra trang liên hệ
	render ra trang contact_us với thông tin về giỏ hàng và các danh mục
	"""
	categories = Category.objects.order_by("id")[:10]
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0}
	return render(request, 'store/contact_us.html', context)

def about_us(request):
	"""
	hàm xuất dữ liệu ra trang giới thiệu
	render ra trang about_us với thông tin về giỏ hàng, và các danh mục
	"""
	categories = Category.objects.order_by("id")[:10]
	cart_quantity = nav(request)#gọi hàm nav bên file utils.py
	context = {'categories': categories, 'cart_quantity': cart_quantity, 'total':0}
	return render(request, 'store/about_us.html', context)	














