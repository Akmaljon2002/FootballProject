from rest_framework.decorators import api_view
from apps.orders import schemas as schm
from apps.orders import services as svc
from apps.users.check_auth import permission


@schm.create_order_schema
@api_view(['POST'])
@permission(['admin'])
def create_order(request):
    return svc.OrderService(request).create_order()


@schm.update_order_schema
@api_view(['PUT'])
@permission(['admin'])
def update_order(request, pk):
    return svc.OrderService(request).update_order(pk)


@schm.delete_order_schema
@api_view(['DELETE'])
@permission(['admin'])
def delete_order(request, pk):
    return svc.OrderService(request).delete_order(pk)


@schm.get_orders_schema
@api_view(['GET'])
@permission(['admin', 'driver'])
def get_orders(request):
    return svc.OrderService(request).get_orders()


@schm.get_order_schema
@api_view(['GET'])
@permission(['admin', 'driver'])
def get_order(request, pk):
    return svc.OrderService(request).get_order(pk)


@schm.accept_order_schema
@api_view(['POST'])
@permission(['driver'])
def accept_order(request, pk):
    return svc.OrderService(request).accept_order(pk)

