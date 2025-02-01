from django.contrib import admin, messages
from . import models
from django.db.models import Q,F,Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from tags.models import Tag,TagItem




@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
   
    list_display = ['title','products_count']
    ordering = ['title']
    search_fields=['title']
    
    
    @admin.display(ordering= 'products_count')
    def products_count(self,collection):
        url =(
            reverse('admin:store_product_changelist')
            +"?"
            + urlencode({
                'collection_id':str(collection.id)}
            )
              
              )
        return format_html('<a href="{}">{} </a>',url,collection.products_count)
      
    
    def get_queryset(self, request) :
        return super().get_queryset(request).annotate(products_count = Count('product'))



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'membership']
    ordering = ['first_name']
    list_editable = ['membership']
    search_fields=['first_name__istartswith','last_name__istartswith']
    list_per_page =5

    
class InventoryFilter(admin.SimpleListFilter):
    title ='Inventory'
    parameter_name ='inventory'

    def lookups(self, request, model_admin):
        return [(
            '<10','Low'
        )]

    def queryset(self, request, queryset):
        if self.value() =='<10':
            return queryset.filter(inventory__lt=10)
    




@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields=['title','slug']
    exclude =['promotions']
    autocomplete_fields=['collection']
    prepopulated_fields = {"slug": ["title"]}
    search_fields=['title']


    actions =['clear_inventory']
    list_display = ['title','price', 'inventory','inventory_status', 'collection_title']
    ordering = ['title']
    list_editable = ['price']
    list_select_related =['collection']
    list_filter=['collection','last_update', InventoryFilter]

    @admin.display(ordering='inventory')
    def inventory_status (self,product):
        if product.inventory  >5:
            return 'Low'
        else:
            return 'OK'
    
    def collection_title(self,product):
        return product.collection.title

    @admin.action(description='Clear Inventory')
    def clear_inventory(self,request,queryset):
        updated_counts =queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_counts},products were updated successfully',
            messages.SUCCESS
        )

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields=['product']
    extra =0



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['id','placed_at', 'order']
    ordering = ['-placed_at']
    autocomplete_fields=['order']
    inlines=[OrderItemInline]



@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields=['product']