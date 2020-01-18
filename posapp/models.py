from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.


#supplier list
class Supplier(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=250, null= True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    mobile_no = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


#customer list
class Customer(models.Model):
    identity = models.IntegerField(primary_key=True)
    customer = models.CharField(max_length=20)   
    customer_phone = models.IntegerField(blank=True, null=True)
    customer_type=models.CharField(max_length=200, default='customer', blank=True, null=True)
    address = models.TextField(max_length=500, blank=True,null=True)
    email = models.EmailField(max_length=100,unique=True)
    image = models.ImageField(upload_to='customer')



    def __str__(self):
        return self.customer



#products details
class Product(models.Model):
    supplier = models.ForeignKey(Supplier,on_delete = models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    brand_name = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product')
    

    
    def __str__(self):
        return self.name


#sales history
class Sales(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now = True)

    def __str__(self):
        return 'sales {0}'.format(self.id)


#order
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Sales, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'sales {0}'.format(self.id)


