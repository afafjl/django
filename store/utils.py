import json
from. models import *
import urllib.request
import urllib
import uuid
import requests
import hmac
import hashlib


def nav(request):
    """
    hàm xuất số lượng sản phẩm trong giỏ hàng cho thanh nav
    input là request 
    output là số lượng sản phẩm trong giỏ hàng
    """
    if request.user.is_authenticated:#nếu người dùng đã đăng nhập thì lấy thông tin giỏ hàng từ database còn không thì lấy từ cookie
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
    return cart_quantity

def saveOrder(request, order_id ):
    """
    hàm dùng để lưu thông tin đơn hàng
    input là request và id của order
    output là trả về order
    """
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
    return order

def momo(request, price):
    """
    hàm chuyển thông tin sang bên môi trường momo test
    input là giá tiền, request
    output là đường dẫn đã được xử lý qua bên momo
    """
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
    return response.json()['payUrl']
def cartdata(request):
    """
    hàm xuất ra dữ liệu bên trong giỏ hàng
    input là request
    output là thông tin về các sản phẩm có trong giỏ hàng được trả về dạng chuỗi, số lượng và tông tất cả
    """
    try:
        if request.user.is_authenticated:#nếu người dùng đã đăng nhập thì lấy thông tin giỏ hàng từ database còn không thì lấy từ cookie
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
    
    return  productsstring, total, cart_quantity