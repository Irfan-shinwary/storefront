from django.db import models

# Create your models here.

class Promotion(models.Model):

    description = models.CharField (max_length=255)
    discount  = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product  = models.ForeignKey('Product', on_delete= models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']



class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    inventory = models.IntegerField()
    slug= models.SlugField(default='-')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    last_update = models.DateField (auto_now=True)
    collection  = models.ForeignKey(Collection, on_delete= models.PROTECT)
    promotions = models.ManyToManyField (Promotion)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title','-price']





class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD= 'G'
    MEMBERSHIP_CHOICES =[
        (MEMBERSHIP_BRONZE,'Bronze'), 
         (MEMBERSHIP_SILVER,'Silver'),
          (MEMBERSHIP_GOLD,'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField (null=True)
    membership = models.CharField (max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    def __str__(self):
            return f'{self.first_name} {' '}{self.last_name}'
    
    class Meta:
        ordering=['first_name','last_name']
        # db_table='store_customers'
        # indexes = [
        #     models.Index(fields=['last_name','first_name'])
        # ]
       





class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE= 'C'
    PAYMENT_STATUS_FAILED= 'F'
    PAYMENT_CHOICES =[
        (PAYMENT_STATUS_PENDING,'Pending'),
         (PAYMENT_STATUS_COMPLETE,'Complete'),
          (PAYMENT_STATUS_FAILED,'Failed'),
    ]
    placed_at = models.DateTimeField (auto_now_add=True)
    payment_status = models.CharField (max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_STATUS_PENDING)
    order  = models.ForeignKey(Customer, on_delete= models.CASCADE)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.PROTECT)
    order = models.ForeignKey(Order,on_delete= models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)




class Adress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.PositiveSmallIntegerField( default=0)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
  





class Cart(models.Model):
    created_at = models.DateTimeField (auto_now_add=True)



class CartItem(models.Model):

    product = models.ForeignKey (Product, on_delete=models.CASCADE)
    cart  = models.ForeignKey(Cart, on_delete= models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

