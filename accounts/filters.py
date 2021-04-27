import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet) :

    class meta:
        model = Order
        fields = '__all__'
