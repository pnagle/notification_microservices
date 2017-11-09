from django.shortcuts import render
from rest_framework import generics
from .models import Order
from rest_framework import mixins, permissions
from .serializers import OrderSerializer


class order_list(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    """
    View to collect orders and view them, using mixins and keeping allow all for simple purpose
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
