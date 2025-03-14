from rest_framework.decorators import api_view
from apps.fields import schemas as schm
from apps.fields import services as svc
from apps.users.check_auth import permission


@schm.create_field_schema
@api_view(['POST'])
@permission(['admin', 'owner'])
def create_field(request):
    return svc.FieldService(request).create_field()


@schm.update_field_schema
@api_view(['PUT'])
@permission(['admin', 'owner'])
def update_field(request, pk):
    return svc.FieldService(request).update_field(pk)


@schm.delete_field_schema
@api_view(['DELETE'])
@permission(['admin', 'owner'])
def delete_field(request, pk):
    return svc.FieldService(request).delete_field(pk)


@schm.get_fields_schema
@api_view(['GET'])
@permission(['admin', 'owner', 'user'])
def get_fields(request):
    return svc.FieldService(request).get_fields()


@schm.get_field_schema
@api_view(['GET'])
@permission(['admin', 'owner', 'user'])
def get_field(request, pk):
    return svc.FieldService(request).get_field(pk)



