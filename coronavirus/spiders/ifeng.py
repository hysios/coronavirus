# -*- coding: utf-8 -*-
import scrapy
import jsonlike
import re
from scrapy_pyppeteer import BrowserRequest, BrowserResponse
from coronavirus.items import SnapshotItem, EventItem
import dateparser


def dateparse(date):
    return dateparser.parse(date,  settings={'DATE_ORDER': 'YMD'})


def cint(s):
    return 0 if not s else int(s)


def snapshot(ss, region=None, name=None):
    return SnapshotItem(
        dead=cint(ss["siwang"]),
        confirmed=cint(ss["quezhen"]),
        suspect=cint(ss["yisi"]),
        cure=cint(ss["zhiyu"]),
        lastReporter=ss["sys_publisher"],
        updatedDate=dateparse(ss["sys_publishDateTime"]),
        name=name or ss["name2"],
        region=region
    )


def event(ev):
    return EventItem(
        summary=ev["summary"],
        moment=dateparse(ev["moment"])
    )


class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    allowed_domains = ['news.ifeng.com']
    start_urls = [
        'https://news.ifeng.com/c/special/7tPlDSzDgVk?aman=fU9fd3d5eqe06Ucf3cf65']

    custom_settings = {
        'STATS_CLASS': 'coronavirus.stats.InfluxDBStatsCollector'
    }

    def start_requests(self):
        yield BrowserRequest(self.start_urls[0])

    async def parse(self, response: BrowserResponse):
        page = response.browser_tab
        snapshots = await self.parseSnapshots(page)
        events = await self.parseEvents(page)

        # print(data)
        for ss in snapshots:
            yield snapshot(ss, region=ss["name1"], name=ss["name1"])

            # print(ss["child"])
            if not ss.__contains__("child"):
                continue

            for child in ss["child"]:
                yield snapshot(child, region=ss["name1"])
        # yield data

        for ev in events:
            yield event(ev)

        await page.close()

    async def parseSnapshots(self, page):
        return await page.evaluate('''() => {
            return allData["yiqing"];
        }''')

    async def parseEvents(self, page):
        return await page.evaluate('''() => {
            return allData["modules"][0]["data"];
        }''')
