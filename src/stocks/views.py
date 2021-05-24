from django.http import HttpResponseRedirect
from django.shortcuts import render
from plotly.graph_objs import Scatter
from plotly.offline import plot

from .models import Stock


def stocks(request):
    tickers = Stock.objects.distinct(
        'ticker').values_list('ticker', flat=True)
    return render(request, "stocks.html",
                  context={'tickers': tickers})


def stock(request, *args, **kwargs):
    date_list = []
    open_list = []
    close_list = []
    low_list = []
    high_list = []
    ticker = request.GET.get('t', '')
    data = Stock.objects.filter(ticker__iexact=ticker)
    if not ticker or not data.exists():
        return HttpResponseRedirect('/stocks')
    if data.exists():
        xy_data = data.values('date', 'oopen', 'close', 'low', 'high')
        for item in xy_data:
            date_list.append(item['date'])
            open_list.append(item['oopen'])
            close_list.append(item['close'])
            low_list.append(item['low'])
            high_list.append(item['high'])

    plot_div = plot([Scatter(x=date_list, y=high_list,
                             mode='lines', name='high',
                             opacity=0.8, marker_color='green'),
                     Scatter(x=date_list, y=low_list,
                             mode='lines', name='low',
                             opacity=0.8, marker_color='red'),
                     ],
                    output_type='div')
    return render(request, "index.html", context={'plot_div': plot_div})


def diff(request, ticker1, ticker2):

    close1_list = []
    close2_list = []

    data1 = Stock.objects.filter(ticker__iexact=ticker1).order_by('date')
    data2 = Stock.objects.filter(ticker__iexact=ticker2).order_by('date')

    if not (data1.exists() and data2.exists()):
        return

    long = data1 if data1.count() > data2.count() else data2
    short = data2 if not (long is data2) else data1

    date_list = short.filter(date__in=long.values_list('date', flat=True)
                             ).values_list('date', flat=True)

    for item in data1.filter(date__in=date_list).values('close'):
        close1_list.append(item['close'])

    for item in data2.filter(date__in=date_list).values('close'):
        close2_list.append(item['close'])

    date_list = list(date_list)
    diff_list = [i1-i2 for i1, i2 in zip(close1_list, close2_list)]

    plot_div = plot([Scatter(x=date_list, y=diff_list,
                             mode='lines', name='diff',
                             opacity=0.8, marker_color='orange'),
                     ],
                    output_type='div')
    return render(request, "index.html", context={'plot_div': plot_div})


def double(request, ticker1, ticker2):

    close1_list = []
    close2_list = []

    data1 = Stock.objects.filter(ticker__iexact=ticker1).order_by('date')
    data2 = Stock.objects.filter(ticker__iexact=ticker2).order_by('date')

    if not (data1.exists() and data2.exists()):
        return

    long = data1 if data1.count() > data2.count() else data2
    short = data2 if not (long is data2) else data1

    date_list = short.filter(date__in=long.values_list('date', flat=True)
                             ).values_list('date', flat=True)

    for item in data1.filter(date__in=date_list).values('close'):
        close1_list.append(item['close'])

    for item in data2.filter(date__in=date_list).values('close'):
        close2_list.append(item['close'])

    date_list = list(date_list)

    plot_div = plot([Scatter(x=date_list, y=close1_list,
                             mode='lines', name=ticker1,
                             opacity=0.8, marker_color='violet'),
                     Scatter(x=date_list, y=close2_list,
                             mode='lines', name=ticker2,
                             opacity=0.8, marker_color='blue'),
                     ],
                    output_type='div')
    return render(request, "index.html", context={'plot_div': plot_div})