import csv
from datetime import datetime
from pathlib import Path

from itemadapter import ItemAdapter

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.__status_vocabulary = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('status'):
            pep_status = adapter['status']
            self.__status_vocabulary[pep_status] = (
                self.__status_vocabulary.get(pep_status, 0) + 1
            )
            return item

    def close_spider(self, spider):
        time = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        filename = BASE_DIR / f'results/status_summary_{time}.csv'
        with open(filename, mode='w', encoding='utf-8') as f:
            csv.writer(
                f, dialect=csv.unix_dialect, quoting=csv.QUOTE_NONE
            ).writerows(
                (
                    ("Статус", "Количество"),
                    *self.__status_vocabulary.items(),
                    ("Total", sum(self.__status_vocabulary.values()))
                )
            )
