from django.db import models
from django.conf import settings
from allproducts.models import Products

User = settings.AUTH_USER_MODEL

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') 
        

    def __str__(self):
        return f"{self.user} - {self.product.title}"