from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(unique=True, max_length=10)
    sex = models.CharField(max_length=1)
    address = models.CharField(max_length=5000)

    def __str__(self):
        return f"{self.auth_id}"


class Product(models.Model):
    pid = models.CharField(max_length=10, unique=True)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    pname = models.CharField(max_length=50)
    pdescription = models.TextField(max_length=2000)
    pprice = models.FloatField()
    pcategory = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.pid} {self.pname}"


class Customer(models.Model):
    auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(unique=True, max_length=10)
    sex = models.CharField(max_length=1)
    address = models.CharField(max_length=5000)

    def __str__(self):
        return f"{self.auth_id}"



class Cart(models.Model):
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart_item = models.JSONField()

    def __str__(self):
        return f"{self.cust_id} {self.cart_item}"








# class Seller(User):
#     # auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     phone = models.CharField(unique=True, max_length=10)
#     sex = models.CharField(max_length=1)
#     address = models.CharField(max_length=5000)

#     def __str__(self):
#         return f"{self.phone}"


# class Product(models.Model):
#     pid = models.CharField(max_length=10, unique=True)
#     seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
#     pname = models.CharField(max_length=50)
#     pdescription = models.TextField(max_length=2000)
#     pprice = models.FloatField()
#     pcategory = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.pid} {self.pname}"



# class Customer(User):
#     # auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     phone = models.CharField(unique=True, max_length=10)
#     sex = models.CharField(max_length=1)
#     address = models.CharField(max_length=5000)

#     def __str__(self):
#         return f"{self.phone}"

