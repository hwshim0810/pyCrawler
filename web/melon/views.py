# -*- coding: utf-8 -*-
from .worker.worker import gathering
from .models import get_daily, parse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request, page=1):
    page = int(page)
    result = get_daily(page)
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
    res = parse(html)

    if res:
        return HttpResponseRedirect('/daily/')
    else:
        return HttpResponse('DB Exception')


