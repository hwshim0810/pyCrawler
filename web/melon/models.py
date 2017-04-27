from django.db import models
from django.utils import timezone
import math


class DailyRank(models.Model):
    rank = models.IntegerField()
    singer = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    album = models.CharField(max_length=150)
    albumImg = models.TextField()
    crawledDate = models.DateField(default=timezone.now)

    def get_dailydata(self, page):
        per_page = 100
        start_num = (page - 1) * 100
        end_num = start_num + per_page
        next_page = page + 1

        total_page = int(math.ceil(float(self.objects.all().count() / per_page)))
        if total_page == 0:
            total_page = 1

        if next_page > total_page:
            next_page = -1

        return {'ranks': self.objects.all().order_by('-crawledDate', 'rank')[start_num:end_num],
                'next_page': next_page,
                'total_page': total_page}

    def publish(self):
        self.save()

    def __str__(self):
        return self.title


