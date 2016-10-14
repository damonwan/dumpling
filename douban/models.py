from django.db import models

class Book(models.Model):
    item_id = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    info = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    rating_numbers = models.IntegerField()
    tags = models.CharField(max_length=500)
    gmt_create = models.DateField(auto_now_add=True)
    gmt_modified = models.DateField(auto_now=True)
    def __str__(self):
        return self.name