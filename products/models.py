from django.db import models

class Car(models.Model):
    title=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    count=models.IntegerField(default=0)
    desc=models.TextField()

    def __str__(self):
        return self.title
