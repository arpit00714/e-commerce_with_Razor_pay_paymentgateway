from django.db import models

class AddItem(models.Model):
    Image = models.ImageField(upload_to='images/')
    Name = models.CharField(max_length=50)
    Price = models.IntegerField()

class Product(models.Model):
    amount = models.IntegerField()
    order_id = models.CharField(max_length=100)
    # payment_id = models.CharField(max_length=100)

class Registration(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Password = models.CharField(max_length=20)

