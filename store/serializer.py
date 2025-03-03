from django.forms import ValidationError
from rest_framework import serializers
from decimal import Decimal
from store.models import Cart, CartItem, Product, Collection, Review


# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()

# class ProdcutSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
#     unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     # 1.  Primary Key Related Fields

#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset = Collection.objects.all()
#     # )

#     # 2. String 

#     # collection = serializers.StringRelatedField(
        
#     # )
# # 3. Nested Object 

#     # collection = CollectionSerializer(
        
#     # )
# # 4. Hyper link
#     collection = serializers.HyperlinkedRelatedField(
#         queryset= Collection.objects.all(),
#         view_name = 'collection-detail'
        
#     )
#     def calculate_tax(self,product:Product):
#         return product.price * Decimal(1.1)
    

# Serializing Related Fields
# 4 ways
# 1.  Primary Key
# 2. String 
# 3. Nested Object 
# 4. Hyper link

# Model serializers
class ProdcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =['id','title','price','price_with_tax','inventory','description','collection']
        
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self,product:Product):
        return product.price * Decimal(1.1)
    

    def create(self, validated_data):
        product= Product(**validated_data)
        product.other =1
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price')
        instance.save()
        return instance
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields =['id','title','products_count']
    
    products_count = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.save()
        return instance

    def create(self, validated_data):
        validated_data = {'title':validated_data.get('title')}
        collection= Collection(**validated_data)
        collection.save()
        return collection


   



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['id','name','description','date']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id, **validated_data)

class SimpleProdcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =['id','title','price']
        

class CartItemSerializer(serializers.ModelSerializer):
    product= SimpleProdcutSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price (self,cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price
    class Meta:
        model= CartItem
        fields=['id', 'product','quantity','total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only =True)
    items = CartItemSerializer(many=True, read_only=True)

    total_price = serializers.SerializerMethodField()

    def get_total_price (self,cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])
       
    
    class Meta:
        model= Cart
        fields=['id', 'items','total_price']




class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
    

    # def validate_product_id(self, value):
    #     if not Product.objects.filter(pk = value).exists():
    #         raise  serializers.ValidationError("No Product with the given ID found")
    
    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']

        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id , **self.validated_data)
        return self.instance
