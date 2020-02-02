import requests
import json
from memo import memo
import atexit


class AMap(object):
    localcache_file = './geo.json'

    def __init__(self, key='dda08a27aa21fde3c0ff6131aa8fecb0'):
        super()
        self.key = key
        self.caches = {}
        try:
            with open(self.localcache_file, 'r') as f:
                self.caches = json.load(f)
        except:
            pass

        atexit.register(self.close)

    @memo
    def getgps(self, address, city=None):
        geocodes = self.geo(address, city)['geocodes']
        if len(geocodes) == 0:
            return None

        loc = geocodes[0]['location'].split(',')

        return (float(loc[1]), float(loc[0]))

    @memo
    def geo(self, address, city=None):
        if self.caches.__contains__(address):
            return self.caches[address]

        params = {'key': self.key, 'address': address}

        if city is not None:
            params['city'] = city

        r = requests.get(
            'https://restapi.amap.com/v3/geocode/geo', params=params)
        val = json.loads(r.text)
        self.caches[address] = val
        return val

    def close(self):
        with open(self.localcache_file, 'w') as f:
            json.dump(self.caches, f)
