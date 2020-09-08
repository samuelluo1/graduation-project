from rest_framework import viewsets
from .serializers import InventorySerializer
from .models import Inventory


class InventoryView(viewsets.ModelViewSet):

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
