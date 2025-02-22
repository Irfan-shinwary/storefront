from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review

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
       