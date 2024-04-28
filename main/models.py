from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, unique=True)
    phone_number = models.CharField(max_length=12) 
    email = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    enrollment = models.CharField(max_length=50,  null=True)
    password = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Menu(models.Model):
    CATEGORY_CHOICES = [
        ('veg', 'Veg'),
        ('non-veg', 'Non-veg')
        # add more categories as needed
    ]

    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to='pics')
    category=models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True)
    price=models.IntegerField()
    persons=models.IntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    approved = models.BooleanField('Approve', default=False)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Menu, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
	
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class Status(models.Model):
    ORDER_STATUS_CHOICES = [
        ('preparing', 'Approved'),
        ('ready', 'Preparing'),
        ('delivered', 'Completed')
    ]

    TIME_CHOICES = [
        (5, '5 minutes'),
        (10, '10 minutes'),
        (15, '15 minutes'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='chefs', limit_choices_to={'complete': True, 'approved': True})
    time_needed = models.IntegerField(choices=TIME_CHOICES, default=5)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='preparing')

    def __str__(self):
        return f'Chef for order {self.order.id}'
    
    # @property
    # def get_order_items(self):
    #     return self.order.orderitem_set.filter(order__complete=True, order__approved=True)

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    hostel = models.CharField(max_length=200, null=True)
    room_number = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.hostel