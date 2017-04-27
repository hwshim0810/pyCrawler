from django.db import models, Error
from django.utils import timezone
import math


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


# get ranks from DB
def get_daily(page):
    per_page = 100
    start_num = (page - 1) * 100
    end_num = start_num + per_page
    next_page = page + 1

    total_page = int(math.ceil(float(DailyRank.objects.all().count() / per_page)))
    if total_page == 0:
        total_page = 1

    if next_page > total_page:
        next_page = -1

    return {'ranks': DailyRank.objects.all().order_by('-crawledDate', 'rank')[start_num:end_num],
            'next_page': next_page,
            'total_page': total_page}


# parse html
def parse(html):
    # 순위
    rank_spans = html.find_all('span', {'class': "rank"})
    edited_rank = []
    for span in rank_spans:
        edited_rank.append(span.text)

    # 앨범이미지
    album_imgs = html.find_all('a', {'class': "image_type15"})
    edited_img = []
    for link in album_imgs:
        edited_img.append(link.img.get('src'))

    # 노래제목
    title_divs = html.find_all('div', {'class': "ellipsis rank01"})
    edited_title = []
    for link in title_divs:
        edited_title.append(link.span.strong.a.text)

    # 가수
    singer_divs = html.find_all('div', {'class': "ellipsis rank02"})
    edited_singer = []
    for link in singer_divs:
        edited_singer.append(link.a.text)

    # 앨범명
    album_divs = html.find_all('div', {'class': "ellipsis rank03"})
    edited_album = []
    for link in album_divs:
        edited_album.append(link.a.text)

    return put_ranks({
        'rank': edited_rank, 'singer': edited_singer,
        'title': edited_title, 'album': edited_album, 'albumImg': edited_img})


def put_ranks(res):
    edited_rank = res['rank']
    edited_singer = res['singer']
    edited_title = res['title']
    edited_album = res['album']
    edited_img = res['albumImg']

    for i in range(0, 100):
        song = DailyRank(
            rank=int(edited_rank[i]), singer=edited_singer[i],
            title=edited_title[i], album=edited_album[i], albumImg=edited_img[i])
        try:
            song.save()
        except Error:
            return False

    return True

