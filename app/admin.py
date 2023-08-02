from django.contrib import admin
from app.models import Contact,Product,Customer,Cart,Payment,OrderPlaced
# Register your models here.

admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Customer)
@admin.register(Cart)
class CarModelAdmin(admin.ModelAdmin):
    list_display=['id','user', 'product','quantity','cust']

@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display=['id','user', 'amount','paid']

@admin.register(OrderPlaced)
class OrderPlaced(admin.ModelAdmin):
    list_display=['id','user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']