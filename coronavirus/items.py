# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import geohash

from coronavirus.amap import AMap

# siwang: ""
# quezhen: "120"
# sys_publishDateTime: "2020-01-25 15:14:45"
# name2: ""
# name1: "福建"
# yisi: ""
# sys_NewAdd: true
# zhiyu: ""
# sys_publisher: "郑鹏"
# child: (9) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]


class SnapshotItem(scrapy.Item):
    dead = scrapy.Field()
    suspect = scrapy.Field()
    confirmed = scrapy.Field()
    cure = scrapy.Field()
    updatedDate = scrapy.Field()
    name = scrapy.Field()
    lastReporter = scrapy.Field()
    childrens = scrapy.Field()
    parent = scrapy.Field()
    amap = AMap()

    def geohash(self):
        gps = self.gps()

        if gps is None:
            return 's0000'
        else:
            return geohash.encode(gps[0], gps[1])

    def gps(self):
        return self.amap.getgps(self['name'])


class EventItem(scrapy.Item):
    summary = scrapy.Field()
    moment = scrapy.Field()
