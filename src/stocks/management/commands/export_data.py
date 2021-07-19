import csv
import datetime
import os

from django.core.management import BaseCommand

from stocks.models import Stock


class Command(BaseCommand):
    """Initial data parsing command. Consuming datafiles
    to fill in the DB. Every datafile contains rows
    <TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
     /example directory contains an example datafile """

    def add_arguments(self, parser):

        parser.add_argument(
            '--dir', type=str,
            help='Path to directory containing files to parse', default='')

    def handle(self, *args, **kwargs):

        dir_path = kwargs['dir']
        if not dir_path or not os.path.isdir(dir_path):
            self.stdout.write(
                'There is no such directory path')
            return

        for file in os.listdir(dir_path):
            with open(os.path.join(dir_path, file), newline='\n') as f:
                reader = csv.reader(f)
                data = list(reader)
                bulk_list = []
                for item in data[1:]:
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
