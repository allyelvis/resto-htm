from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MenuItem, Stock, Order

@api_view(['GET'])
def get_menu_items(request):
    menu_items = MenuItem.objects.all().values()
    return Response({"menu": list(menu_items)})

@api_view(['POST'])
def create_order(request):
    item_id = request.data['menu_item_id']
    quantity = request.data['quantity']
    menu_item = MenuItem.objects.get(id=item_id)
    total_price = menu_item.price * quantity
    order = Order.objects.create(menu_item=menu_item, quantity=quantity, total_price=total_price, status='Pending')
    return Response({"order_id": order.id, "status": "Order created"})

@api_view(['GET', 'PUT'])
def manage_stock(request):
    if request.method == 'GET':
        stock_items = Stock.objects.all().values()
        return Response({"stock": list(stock_items)})
    elif request.method == 'PUT':
        stock_item_id = request.data['stock_item_id']
        quantity = request.data['quantity']
        stock = Stock.objects.get(id=stock_item_id)
        stock.quantity += quantity
        stock.save()
        return Response({"status": "Stock updated"})
