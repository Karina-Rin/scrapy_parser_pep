import csv
import datetime as dt
from collections import Counter
from pathlib import Path

from scrapy.exceptions import DropItem

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.status = Counter()

    def process_item(self, item, spider):
        if "status" not in item:
            raise DropItem("Этот статус не найден")
        pep_status = item["status"]
        self.status[pep_status] += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / "results"
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        time = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = results_dir / f"status_summary_{time}.csv"
        with file_name.open(mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, dialect="unix")
            rows = [(status, count) for status, count in self.status.items()]
            rows.insert(0, ("Статус", "Количество"))
            rows.append(("Total", sum(self.status.values())))
            writer.writerows(rows)
