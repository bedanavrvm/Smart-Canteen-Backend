from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

# Create your models here.

#User Model
#Handles user registration
class User(AbstractUser):
    reg_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('admin', 'Admin'), ('staff', 'Staff')])
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # It’s used internally by Django’s admin and permission system/Allows user to login to Django's admin panel

    REQUIRED_FIELDS = ['email', 'name', 'role']

    def save(self, *args, **kwargs):
        # Automatically set username to reg_number if not provided
        if not self.username:
            self.username = self.reg_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.reg_number})"


# Tag Model for categorizing menu items
class Tag(models.Model):
    TAG_TYPES = [
        ('meal_type', 'Meal Type'),
        ('time_of_day', 'Time of Day'),
        ('temperature', 'Temperature'),
    ]
    
    name = models.CharField(max_length=50)
    tag_type = models.CharField(max_length=20, choices=TAG_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['name', 'tag_type']
        ordering = ['tag_type', 'name']
    
    def __str__(self):
        return f"{self.get_tag_type_display()}: {self.name}"


#Handles menu
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    image_url = models.ImageField(upload_to='menu_item_pictures/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='menu_items', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

#Handles orders
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices= [
        ('pending', 'Pending'), 
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'), 
        ('ready', 'Ready'), 
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], max_length=20, default='pending')
    order_date = models.DateField(auto_now_add=True)
    pickup_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.name} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_ref = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('m-pesa', 'M-Pesa'), ('card', 'Card'), ('cash', 'Cash')])
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    receipt_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)


class Inventory(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    stock_level = models.PositiveIntegerField()
    threshold = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Inventories'
    def __str__(self):
        return self.name
    

