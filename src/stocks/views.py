from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from plotly.graph_objs import Scatter
from plotly.offline import plot

from .constants import MONTHS
from .models import Stock


def stocks(request):
    """Shows available tickers"""

    tickers = Stock.objects.distinct(
        'ticker').values_list('ticker', flat=True)
    return render(request, "stocks.html",
                  context={'tickers': tickers})


def stock(request, *args, **kwargs):
    """Shows a single stock grid with multiple graphs"""

    mode = 'lines'
    xaxis_title = 'Years'
    date_list = []
    open_list = []
    close_list = []
    low_list = []
    high_list = []
    ticker = request.GET.get('ticker', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')

    if month.isdigit():
        month = int(month)

    data = Stock.objects.filter(ticker__iexact=ticker).order_by('date')
    if year and year.isdigit():
        if month and month in MONTHS:
            data = data.filter(Q(date__year=year,
                                 date__month=month))
            xaxis_title = f'{MONTHS[month]} {year}'
        else:
            data = data.filter(Q(date__year=year))
            xaxis_title = year

    if not ticker or not data.exists():
        return HttpResponseRedirect('/stocks')
    title = f'{ticker} ({year})' if year else f'{ticker}'
    if data.exists():
        xy_data = data.values('date', 'oopen', 'close', 'low', 'high')
        for item in xy_data:
            date_list.append(item['date'])
            open_list.append(item['oopen'])
            close_list.append(item['close'])
            low_list.append(item['low'])
            high_list.append(item['high'])

    figure = {'data': [
        Scatter(x=date_list, y=high_list, mode=mode, name='high',
                opacity=0.8, marker_color='green'),
        Scatter(x=date_list, y=low_list, mode=mode, name='low',
                opacity=0.8, marker_color='red', visible='legendonly'),
        Scatter(x=date_list, y=open_list, mode=mode, name='open',
                opacity=0.8, marker_color='blue', visible='legendonly'),
        Scatter(x=date_list, y=close_list, mode=mode, name='close',
                opacity=0.8, marker_color='orange', visible='legendonly'),
    ], 'layout': {'title': {'text': title, 'y': 0.9, 'x': 0.5,
                            'xanchor': 'center', 'yanchor': 'top'},
                  'yaxis_title': "Value", 'xaxis_title': xaxis_title
                  }}

    plot_div = plot(figure, output_type='div')
    return render(request, "index.html", context={'plot_div': plot_div})


def analyze(request, *args, **kwargs):
    """Shows grid with all available tickers. Every graph reflects the percentage
    ratio between the opening price and the closing price of stock"""

    mode = 'lines+markers'

    tickers = Stock.objects.distinct(
        'ticker').values_list('ticker', flat=True)
    tickers_dict = {ticker: [] for ticker in tickers}
    tickers_count = tickers.count()

    actual_dates = Stock.objects.values('date').annotate(
        dcount=Count('date')).filter(dcount=tickers_count).values_list(
        'date', flat=True).order_by('date')
    date_list = list(actual_dates)

    data = Stock.objects.filter(date__in=actual_dates).order_by('date')

    for item in data.values('ticker', 'close', 'oopen'):
        tickers_dict[item['ticker']].append(
            round((item['close']-item['oopen'])*100/item['oopen'], 2)
        )

    scatters = [Scatter(x=date_list, y=tickers_dict[obj], mode=mode, name=obj,
                opacity=0.8, visible='legendonly') for obj in tickers_dict]
    figure = {'data': scatters, 'layout': {
        'title': {
            'text': 'Open-Closed comparision', 'y': 0.9, 'x': 0.5,
            'xanchor': 'center','yanchor': 'top'},
        'yaxis_title': "Daily percent",
        'xaxis_title': "Years",
    }}

    return render(request, "analyze.html", context={
        'plot_div': plot(figure, output_type='div')})
