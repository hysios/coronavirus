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

        self.esClient = Elasticsearch(ELASTIC['hosts'], port=ELASTIC['port'])

        self.esClient.indices.create(index="ncov2019", ignore=400, body={
            "mappings": {
                "properties": {
                    "location": {
                        "type": "geo_point"
                    },
                    "@timestamp": {
                        "format": "strict_date_optional_time||epoch_millis",
                        "type": "date",
                    },
                }
            }
        })

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
                'parent': item['parent'] or item['name'],
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
        loc = item.gps()
        doc = {
            'dead': item['dead'],
            'suspect': item['suspect'],
            'confirmed': item['confirmed'],
            'name': item['name'],
            'cure': item['cure'],
            "time": item['updatedDate'],
            '@timestamp': time,
        }

        if loc is not None:
            doc['location'] = {
                "lat": loc[0],
                "lon": loc[1]
            }

        self.esClient.index(index="ncov2019", body=doc)

    def process_event(self, item, spider):
        measurements = [{
            "measurement": "events",
            # "tags": {
            #     "city": item['name'],
            # },
            "time": item['moment'],
            "fields": {
                'summary': item['summary'],
                # 'moment': item['moment'],
            }
        }]

        self.client.write_points(measurements)
