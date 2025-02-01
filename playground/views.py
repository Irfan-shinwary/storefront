from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q,F,Count
from store.models import Customer
from store.models import Product
# Create your views here.

def say_hello(request):
   
    # return  HttpResponse('Hello World !')
    query_set = Customer.objects.all()
    # query_set = Customer.objects.filter(id=1).first()   
    # exists = Customer.objects.filter(id=1).exists()   
    # query_set = Customer.objects.get(id=1)

    



    # query_set = Customer.objects.count()

    # for customer in query_set:
    #     print(customer)

    # query_set = Product.objects.filter(inventory =20 ,price__gt = 10)

    # &~

    query_set = Product.objects.filter(Q(inventory__lt =20) | Q(price__gt = 10))
    query_set = Product.objects.filter(inventory = F('price'))
    query_set = Product.objects.order_by('price','-inventory').reverse()

    product = Product.objects.order_by('-title')[0]
    product = Product.objects.earliest('price')
    product = Product.objects.latest('price')

    query_set = Product.objects.all()





    # queryset api:
    # __gt, __gte,__lt,__lte,__in,__range,__in, __contains,__icontains, __startwith, __endwith,__year,month,day,hour,minute, __isnull=True

    return  render(request,'hello.html',{'name':'Irfanullah','products': query_set,'product':product})