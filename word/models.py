from django.db import models
from django.urls import reverse


class Word(models.Model):
    word = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.word

    def get_absolute_url(self):
        return reverse('wiki', kwargs={'word': self.word})
