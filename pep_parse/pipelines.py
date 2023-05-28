import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

from scrapy.exceptions import DropItem

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.status = defaultdict()

    def process_item(self, item, spider):
        if "status" not in item:
            raise DropItem("Статус не найден")
        pep_status = item["status"]
        self.status[pep_status] = self.status.get(pep_status, 0) + 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / "results"
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        time = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = results_dir / f"status_summary_{time}.csv"
        with open(file_name, mode="w", encoding="utf-8") as file:
            writer = csv.writer(file, dialect="unix")
            writer.writerows(
                (
                    ("Статус", "Количество"),
                    *self.status.items(),
                    ("Total", sum(self.status.values())),
                )
            )
