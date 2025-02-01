from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

class ProdcutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # 1.  Primary Key Related Fields

    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    # 2. String 

    # collection = serializers.StringRelatedField(
        
    # )
# 3. Nested Object 

    # collection = CollectionSerializer(
        
    # )
# 4. Hyper link
    collection = serializers.HyperlinkedRelatedField(
        queryset= Collection.objects.all(),
        view_name = 'collection-detail'
        
    )
    def calculate_tax(self,product:Product):
        return product.price * Decimal(1.1)
    

# Serializing Related Fields
# 4 ways
# 1.  Primary Key
# 2. String 
# 3. Nested Object 
# 4. Hyper link