from django.db import models

# Create your models here.
class Category (models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Slang(models.Model):
    term = models.CharField(max_length=100, unique=True)
    meaning = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='slangs')
    origin = models.CharField(max_length=200, blank=True)
    popularity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    usage_example = models.TextField(blank=True)
    cultural_origin = models.CharField(max_length=200, blank=True)
    trendiness_score = models.IntegerField(default=0)
    def __str__(self):
        return self.term