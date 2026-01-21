from django.db import models

class Word(models.Model):
    text = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.text} ({self.category})"
