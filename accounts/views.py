from django.shortcuts import render, redirect

from django.http import HttpResponse

from  .models import *
from .forms import OrderForm
from .filters import OrderFilter
import requests as rq
# Create your views here.

def home(request):

    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    total_delivered = orders.filter(status = 'Delivered').count()
    total_pending = orders.filter(status = 'Pending').count()
    context = {
        'customers' : customers,
         'orders' : orders,
        'total_orders' : total_orders,
        "total_delivered":total_delivered,
        "total_pending" : total_pending

    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):

    allProducts = Product.objects.all()

    return render(request, 'accounts/products.html', {"allProducts": allProducts})


def customers(request, pk):

    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()
    num_of_orders = orders.count()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {'customer' : customer, "orders": orders,"num_of_orders":num_of_orders,
               "my_filter": my_filter }

    return render(request, 'accounts/customers.html', context)


def createOrder(request, pk):

    customer = Customer.objects.get(id=pk)

    form = OrderForm(initial={'customer' : customer})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form" : form}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):

    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form": form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)
    context = {"item": order}
    if request.method == "POST":
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', context)