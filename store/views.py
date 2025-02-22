from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection,OrderItem, Review
from django.db.models import Q,F,Count

from .serializer import CollectionSerializer, ProdcutSerializer, ReviewSerializer
# Create your views here.

# @api_view(['GET','POST']) 
# def product_list(request):
#     # return  HttpResponse('Products')
#     if request.method=='GET':
#         queryset= Product.objects.select_related('collection').all()
#         serializer = ProdcutSerializer(queryset, many=True, context={'request':request})
#         return  Response(serializer.data)
#     elif request.method=='POST':
#         serializer=  ProdcutSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response (serializer.data)

# @api_view(['PUT','GET','DELETE'])
# def product_details(request,id):
#     # try:
#     # product = Product.objects.get(pk=id)

#     product = get_object_or_404(Product,pk=id)
#     if request.method =='GET':
#         serializer = ProdcutSerializer(product)
#         return  Response(serializer.data)
#     elif request.method =='PUT':
#         serializer= ProdcutSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif request.method=='DELETE':
#         if product.orderitem_set.count()>0:
#             return Response({"error":"The product can't be deleted because it is associated with an order item."}, status=status.HTTP_403_FORBIDDEN)
#         product.delete()
#         return Response (status= status.HTTP_204_NO_CONTENT)

    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)



# @api_view(['GET','POST']) 
# def collection_list(request):
#     # return  HttpResponse('Products')
#     if request.method == 'GET':
#         queryset= Collection.objects.annotate(products_count=Count('product')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return  Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer=  CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response (serializer.data)



    
# @api_view(['GET','PUT','DELETE'])
# def collection_details(request,pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')),pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return  Response(serializer.data)
    
#     elif request.method =='PUT':
#         serializer= CollectionSerializer(collection,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif request.method=='DELETE':
#         # if collection.product_set.count()>0:
#         collection.delete()
#         return Response (status= status.HTTP_204_NO_CONTENT)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)



# API Views Class

# class ProductList(APIView):

#     def get(self, request):
#         queryset= Product.objects.select_related('collection').all()
#         serializer = ProdcutSerializer(queryset, many=True, context={'request':request})
#         return  Response(serializer.data)
    
#     def post(self,request):
#         serializer=  ProdcutSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response (serializer.data)

# class ProductDetails(APIView):
#     def get (self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProdcutSerializer(product)
#         return  Response(serializer.data)

#     def put(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer= ProdcutSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete (self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         if product.orderitem_set.count()>0:
#             return Response({"error":"The product can't be deleted because it is associated with an order item."}, status=status.HTTP_403_FORBIDDEN)
#         product.delete()
#         return Response (status= status.HTTP_204_NO_CONTENT)






# ListCreateAPIView Generic Class

# class ProductList(ListCreateAPIView):

#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()
    
#     def get_serializer_class(self):
#         return ProdcutSerializer

#     def get_serializer_context(self):
#         return {'request':self.request}

# class ProductDetails(RetrieveUpdateDestroyAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProdcutSerializer
    # # lookup_field ='id'

    # def delete (self,request,pk):
    #     product = get_object_or_404(Product,pk=pk)
    #     if product.orderitem_set.count()>0:
    #         return Response({"error":"The product can't be deleted because it is associated with an order item."}, status=status.HTTP_403_FORBIDDEN)
    #     product.delete()
    #     return Response (status= status.HTTP_204_NO_CONTENT)
    

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer


# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#     # lookup_field ='id'

#     def delete (self,request,pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')),pk=pk)
#         if collection.product_set.count()>0:
#             return Response({"error":"The Collection can't be deleted because it is associated with product item."}, status=status.HTTP_403_FORBIDDEN)
#         collection.delete()
#         return Response (status= status.HTTP_204_NO_CONTENT)


# APIViewSET

class ProductViewSet(ModelViewSet):
    serializer_class = ProdcutSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = collection_id = self.request.query_params.get('collection_id')

        if collection_id is not None:
            queryset = Product.objects.filter(collection_id= collection_id).all()
        return queryset

    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({"error":"The product can't be deleted because it is associated with an order item."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    

    

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {'request':self.request}
    
    def delete (self,request,pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')),pk=pk)
        if collection.product_set.count()>0:
            return Response({"error":"The Collection can't be deleted because it is associated with product item."}, status=status.HTTP_403_FORBIDDEN)
        collection.delete()
        return Response (status= status.HTTP_204_NO_CONTENT)
    
# We can Use ReadOnlyModelViewSet when we just need to read the model not create,update nad delete



# Adding Review to Product
class ReviewVieSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id= self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
   
