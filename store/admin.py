from django.contrib import admin
from . import models
from django.db.models import Q,F,Count
from django.utils.html import format_html, urlencode
from django.urls import reverse




@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    ordering = ['title']
    
    @admin.display(ordering= 'products_count')
    def products_count(self,collection):
        url =(
            reverse('admin:store_product_changelist')
            +"?"
            + urlencode({
                'collection_id':str(collection.id)}
            )
              
              )
        format_html('<a href={}>{} </a>',url,collection.products_count)
        return collection.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count = Count('product'))



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'membership']
    ordering = ['first_name']
    list_editable = ['membership']
    list_per_page =5

    


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price', 'inventory_status', 'collection_title']
    ordering = ['title']
    list_editable = ['price']
    list_select_related =['collection']

    @admin.display(ordering='inventory')
    def inventory_status (self,product):
        if product.inventory  >5:
            return 'Low'
        else:
            return 'OK'
    
    def collection_title(self,product):
        return product.collection.title
    


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at', 'order']
    ordering = ['-placed_at']
