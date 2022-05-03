from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	# path('account/', views.account, name="account"),
	# path('blog_single/', views.blog_single, name="blog_single"),
	path('blog_single/', views.blog_single, name="blog_single"),
	path('contact/', views.contact, name="contact"),
	path('product_single/', views.product_single, name="product_single"),
	path('products/', views.products, name="products"),
	# path('wishlist/', views.wishlist, name="wishlist"),
	path('about_us/', views.about_us, name="about_us"),
	path('blog_details/', views.blog_details, name="blog_details"),
	path('update_item/', views.updateItem, name="update_item"),
	path('blog/', views.blog, name="blog"),
	path('login/', views.loginPage, name="loginPage"),
	path('logout/', views.logoutUser, name="logout"),
	path('register/', views.register, name="register"),
	path('services/', views.services, name="services"),
]	