# -*- coding: utf-8 -*-
import requests
import math
from bs4 import BeautifulSoup
from melon.models import DailyRank
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.decorators import login_required


def gathering():
    url = "http://www.melon.com/chart/day/index.htm"
    src = requests.get(url)
    souped = BeautifulSoup(src.text, 'lxml')
    return souped


def get_dailydata(page):
    per_page = 100
    start_num = (page-1) * 100
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


# Create your views here.
def index(request, page=1):
    page = int(page)
    result = get_dailydata(page)
    ranks = result['ranks']
    crawled_date = ''

    if (len(ranks) != 0):
        crawled_date = ranks[0].crawledDate

    tpl = loader.get_template('index.html')
    ctx = Context({
        'ranks': ranks,
        'current_page': page,
        'chart_date': crawled_date,
        'next_page': result['next_page'],
        'priv_page': page-1,
        'total_page': result['total_page']
    })

    return HttpResponse(tpl.render(ctx))


@login_required(login_url='/accounts/login/')
def is_gather(request):
    return render(request, 'alert_gather.html')


@login_required(login_url='/accounts/login/')
def do_gather(request):
    html = gathering()

    # 차트날짜
    chart_date = html.find_all('span', {'class': "datelk"})[0].text

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

    for i in range(0, 100):
        song = DailyRank(rank=int(edited_rank[i]), singer=edited_singer[i], title=edited_title[i],
                         album=edited_album[i], albumImg=edited_img[i])
        try:
            song.save()
        except Exception:
            return HttpResponse('DB Exception')

    return HttpResponseRedirect('/daily/')
