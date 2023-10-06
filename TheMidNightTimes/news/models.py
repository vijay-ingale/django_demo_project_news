from django.db import models
from django.contrib.auth.models import User


class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=300)
    created_at = models.DateTimeField()


class SearchResults(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_published = models.DateTimeField(null=True, blank=True)


