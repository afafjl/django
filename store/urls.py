from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	# path('account/', views.account, name="account"),
	# path('blog_single/', views.blog_single, name="blog_single"),

	path('contact/', views.contact, name="contact"),

	path('products/', views.products, name="products"),
	# path('wishlist/', views.wishlist, name="wishlist"),
	path('about_us/', views.about_us, name="about_us"),

	path('update_item/', views.updateItem, name="update_item"),
	path('blog/', views.blog, name="blog"),
	path('login/', views.loginPage, name="loginPage"), 
	path('logout/', views.logoutUser, name="logout"),
	path('register/', views.register, name="register"),

	path('blog_details/<int:pk>', views.blog_details, name="blog_details"),
	path('single_product/<int:pk>', views.single_product, name="single_product"),
	path('single_product/<int:pk>/<int:stars>', views.review_stars, name="review_stars"),
	path('category/<int:pk>', views.category, name="category"),
	path('search', views.search, name="search"),
	path('vnpay', views.payment, name="vnpay"),
	path('feedback', views.feedback, name="feedback"),
	path('address_info/<int:pk>', views.address_info, name="address_info"),
	path('orders', views.orders, name="orders"),
	path('shipped/<int:pk>', views.shipped, name="shipped"),
]	