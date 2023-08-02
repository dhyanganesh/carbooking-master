from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('MZ', 'maruti suzuki'),
    ('HY', 'hyunda'),
    ('AD', 'audi'),
    ('JR', 'jaguar'),
    ('JP', 'jeep'),
    ('BM', 'bmw'),
    ('MS', 'mercedes'),
    ('SK', 'skoda'),
    ('VO', 'volvo'),
    ('HO', 'honda'),
    ('LM', 'lamborghini'),
    ('PE', 'porsche'),
)
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12)
    description = models.TextField()

    def __str__(self):
        return f'Message from {self.name}'


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_prize = models.FloatField()
    discription = models.TextField()
    composition = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_images = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phoneno = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cust = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_prize

STATUS_CHOICES = (
('Accepted', 'Accepted'),
('Packed', 'Packed'),
('On The Way', 'On The Way'),
('Delivered', 'Delivered'),
('Cancel', 'Cancel'),
('Pending', 'Pending'),
)

class Payment (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    paid = models.BooleanField(default=False)


class OrderPlaced (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models. PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Sucessfull") 
    payment = models.ForeignKey(Payment, on_delete=models. CASCADE, default="",null=True) 
    
    @ property
    def total_cost(self):
        return self.quantity * self.product.selling_prize
