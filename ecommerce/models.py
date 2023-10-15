from django.db import models

class ProductCat(models.Model):
    poduct_cat_type = models.CharField(max_length=200, default="")
    producT_cat_image = models.ImageField(upload_to="cat/images/" , default="")
    
    def __str__(self):
        return self.poduct_cat_type
    
class Product(models.Model):
    product_name = models.CharField(max_length=200 , default="")
    product_image = models.ImageField(upload_to="images/")
    product_desc = models.CharField(max_length=200, default="")
    product_seller = models.CharField(max_length=200, default="")
    product_reviews = models.IntegerField(default="")
    product_cat = models.ForeignKey(ProductCat, on_delete=models.CASCADE, default="")
    product_price = models.IntegerField(default="")
    
    
    def __str__(self):
        return self.product_name
    


class Users(models.Model):
    username = models.CharField(max_length=200, default="")
    email = models.EmailField(max_length=200, default="")
    name = models.CharField(max_length=200, default="")
    password = models.CharField(max_length=200, default="")
    contact = models.CharField(max_length=200, default="")
    
    
    def __str__(self):
        return self.username
    
class Cart(models.Model):

    user_assoc = models.ForeignKey(Users, on_delete=models.CASCADE)
    product_assoc = models.ForeignKey(Product, on_delete=models.CASCADE , default="")
    quantity = models.IntegerField( default=1)
    purchased  = models.BooleanField(default=False)
    

class Orders(models.Model):
    username = models.ForeignKey(Users , on_delete=models.CASCADE)
    address = models.CharField(max_length=500, default=""),
    city = models.CharField(max_length=500, default=""),
    zipcode =  models.CharField(max_length=500, default="")
    state = models.CharField(max_length=500, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
     
    
    
