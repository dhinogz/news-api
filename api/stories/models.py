from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    key = models.BigAutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    details = models.CharField(max_length=128)
    category = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.headline

    class Meta:
        verbose_name_plural = "stories"
        indexes = [
            models.Index(fields=['region']),
            models.Index(fields=['date']),
            models.Index(fields=['category']),
        ]
