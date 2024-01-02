from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank = True, null = True)
    borrowing_price = models.DecimalField(max_digits=8, decimal_places=2)
    categories = models.ManyToManyField(Category)
    author = models.CharField(max_length=100,null=True,blank=True)
    reviews = models.ManyToManyField(User, through='Review')

    def __str__(self):
        return self.title 
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    
    def __str__(self):
        return f"Reviewed by {self.user.username}"
    
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    returned_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Borrowed by {self.user.username}"
