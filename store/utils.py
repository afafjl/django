import json
from. models import *
#hàm xuất dữ liệu cho thanh nav
def nav(request):
    products = Product.objects.all()
    total =0
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer= customer, complete = False)
    #     cartItems = order.get_cart_items
    # else:		
    #     try:
    #         cart = json.loads(request.COOKIES['cart'])
    #         # cartItems = 0
    #     except:
    #         cart={}
    #         cartItems = 0
    #         for i in cart:
    #             cartItems += cart[i]["quantity"]
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
            # try:
            #     cart = json.loads(request.COOKIES['cart'])
            # except:
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

    # context = {'productsstring': productsstring, 'total':total, 'cartItems': cartItems}
    return {'products': products, 'cartItems': cartItems, 'productsstring': productsstring, 'total':total}
