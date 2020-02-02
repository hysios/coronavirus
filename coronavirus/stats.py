# note that I stored this class in the scrapers.metrics module
from influxdb import InfluxDBClient
import datetime
from scrapy.statscollectors import StatsCollector
from coronavirus.settings import INFLUXDB


class InfluxDBStatsCollector(StatsCollector):
    def __init__(self, crawler):
        super(InfluxDBStatsCollector, self).__init__(crawler)

        self.client = InfluxDBClient(
            INFLUXDB['host'], INFLUXDB['port'], INFLUXDB['username'], INFLUXDB['password'], INFLUXDB['database'])

    def _persist_stats(self, stats, spider):
        time = datetime.datetime.utcnow().isoformat()

        measurements = [{
            "measurement": "scrapy_spiders",
            "tags": {
                "spider_name": spider.name
            },
            "time": time + "Z",
            "fields": {
                'request_bytes': stats.get('downloader/request_bytes', 0),
                'response_bytes': stats.get('downloader/response_bytes', 0),
                'elapsed_time_in_seconds': stats.get('elapsed_time_seconds', 0),
                'item_scraped_count': stats.get('item_scraped_count', 0),
                'max_title_length': stats.get('max_title_length', 0),
                'min_title_length': stats.get('min_title_length', 0),
                'empty_title': stats.get('item_dropped_reasons_count/EmptyTitle', 0),
                'item_dropped_count': stats.get('item_dropped_count', 0)
            }
        }]

        self.client.write_points(measurements)
