import csv
import datetime
import os
import sys

from django.core.management import BaseCommand

from stocks.models import Stock


class Command(BaseCommand):
    """Парсинг данных."""

    def handle(self, *args, **kwargs):
        """Выполнение."""

        dir_path = '/home/anton/Documents/development/stock_exchange/files'
        for file in os.listdir(dir_path):
            with open(os.path.join(dir_path, file), newline='\n') as f:
                reader = csv.reader(f)
                data = list(reader)
                bulk_list = []
                for item in data[1:]:
                    sys.stdout.write(str(item))
                    bulk_list.append(Stock(
                        ticker=item[0],
                        per=item[1],
                        date=datetime.date(
                            int(item[2][0:4]),
                            int(item[2][4:6]),
                            int(item[2][6:8])),
                        oopen=item[4],
                        high=item[5],
                        low=item[6],
                        close=item[7],
                        vol=item[8]
                    ))
                Stock.objects.bulk_create(bulk_list)
                sys.stdout.write(str(len(bulk_list)))
