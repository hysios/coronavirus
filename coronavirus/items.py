# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import geohash

from coronavirus.amap import AMap


class SnapshotItem(scrapy.Item):
    dead = scrapy.Field()
    suspect = scrapy.Field()
    confirmed = scrapy.Field()
    cure = scrapy.Field()
    updatedDate = scrapy.Field()
    name = scrapy.Field()
    lastReporter = scrapy.Field()
    childrens = scrapy.Field()
    region = scrapy.Field()
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
