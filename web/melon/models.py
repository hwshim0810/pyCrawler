from django.db import models
from django.utils import timezone


class DailyRank(models.Model):
    rank = models.IntegerField()
    singer = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    album = models.CharField(max_length=150)
    albumImg = models.TextField()
    crawledDate = models.DateField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title


