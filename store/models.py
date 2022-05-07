from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    # slug = models.SlugField()
    # parent = models.ForeignKey('self',blank=True, null=True ,related_name='children',on_delete=models.SET_NULL)

    def __str__(self):                                         
        return self.name  
class Customer(models.Model):
    user = models.OneToOneField(User, null= True, blank= True, on_delete= models.CASCADE)
    name = models.CharField( max_length=100, null= True)
    email = models.CharField( max_length=100, null= True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField( max_length=100, null= True)
    price = models.IntegerField( null= True)
    unsale_price = models.IntegerField( null= True)
    stars = models.FloatField(default=0, null= True)
    review_times = models.IntegerField(default=0, null= True)
    image = models.ImageField(null=True, blank = True,)
    category = models.ForeignKey(Category,related_name = "products", blank=True, null= True, on_delete=models.SET_NULL)
    description = models.TextField( max_length=2000, null= True)
    short_description = models.CharField( max_length=500, null= True)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    def aaa(self):
        return 5-round(self.stars,0)
    def aaaa(self):
        return round(self.stars,0)

class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null= True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField( auto_now_add=True, null= True)
    complete = models.BooleanField(default= False, null = True, blank = False)
    transaction_id = models.CharField( max_length=100, null= True)
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, blank=True, null= True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, blank=True, null= True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default= 0, null=True, blank= True)
    date_added= models.DateTimeField( auto_now_add=True, null= True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(Customer, blank=True, null= True, on_delete=models.SET_NULL)
#     order = models.ForeignKey(Order, blank=True, null= True, on_delete=models.SET_NULL)
#     address = models.CharField( max_length=400, null= True)
#     name = models.CharField( max_length=50, null= True)
#     phone = models.CharField( max_length=15, null= True)
#     city = models.CharField( max_length=100, null= True)
#     date_added = models.DateTimeField( auto_now_add=True, null= True)
#     def __str__(self):
#         return self.address
class Address(models.Model):
    address = models.CharField( max_length=300, null= True)
    name = models.CharField( max_length=300, null= True)
    phone = models.CharField( max_length=300, null= True)
    time = models.DateTimeField(auto_now_add=True,null= True)
    city = models.CharField( max_length=300, null= True)
     
    def __str__(self):
        return self.address
class Blog(models.Model):
    title = models.CharField( max_length=100, null= True)
    description = models.TextField( null= True)
    short_description = models.CharField( max_length=300, null= True)
    image = models.ImageField(null=True, blank = True)
    time = models.DateTimeField(null= True)
    tags = TaggableManager()
     
    def __str__(self):
        return self.title
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
class Comment(models.Model):
    product = models.ForeignKey(Product, blank=True,related_name = "comments", null= True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null= True, blank= True, on_delete= models.CASCADE)
    description = models.TextField( null= True)
    date_added= models.DateTimeField( auto_now_add=True,null= True)
    def __str__(self):
        return self.description
class Blog_comment(models.Model):
    blog = models.ForeignKey(Blog, blank=True,related_name = "comments", null= True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null= True, blank= True, on_delete= models.CASCADE)
    description = models.TextField( null= True)
    date_added= models.DateTimeField( auto_now_add=True,null= True)
    def __str__(self):
        return self.description
class Review(models.Model):
    product = models.ForeignKey(Product, blank=True, null= True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null= True, blank= True, on_delete= models.CASCADE)
    stars = models.IntegerField(default=0,null= True)
    first_time = models.BooleanField(default= True, null = True, blank = False)
    @property

    def aaa(self):
        return 5 - self.stars
class Feedback(models.Model):
    name = models.CharField( max_length=100, null= True)
    email = models.CharField( max_length=100, null= True)

    comment = models.TextField( max_length=1000, null= True)
     
    def __str__(self):
        return self.name