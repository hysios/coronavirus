# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from influxdb import InfluxDBClient
from coronavirus.settings import INFLUXDB, ELASTIC
from coronavirus.items import SnapshotItem, EventItem
import datetime
from elasticsearch import Elasticsearch
import re


class CoronavirusPipeline(object):

    def __init__(self):
        super(CoronavirusPipeline, self).__init__()

        self.client = InfluxDBClient(
            INFLUXDB['host'], INFLUXDB['port'], INFLUXDB['username'], INFLUXDB['password'], INFLUXDB['database'])

    def process_item(self, item, spider):
        if isinstance(item, SnapshotItem):
            if re.search(r"^「数据更新时间", item['name']) is None:
                self.process_snapshot(item, spider)
        elif isinstance(item, EventItem):
            self.process_event(item, spider)
        return item

    def process_snapshot(self, item, spider):
        time = datetime.datetime.utcnow().isoformat()

        measurements = [{
            "measurement": "snapshots",
            "tags": {
                "city": item['name'],
                'geohash': item.geohash(),
                'region': item['region'] or item['name'],
            },
            "time": time+"Z",
            "fields": {
                'dead': item['dead'],
                'suspect': item['suspect'],
                'confirmed': item['confirmed'],
                'name': item['name'],
                'cure': item['cure'],
                'lastReporter': item['lastReporter'],
                'publishTime': item['updatedDate'].strftime("%Y/%m/%d, %H:%M:%S"),
            }
        }]

        self.client.write_points(measurements)

    def process_event(self, item, spider):
        measurements = [{
            "measurement": "events",
            "time": item['moment'],
            "fields": {
                'summary': item['summary'],
            }
        }]

        self.client.write_points(measurements)
