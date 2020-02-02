FROM python:3.7.6-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git build-essential libx11-6 \
    gconf-service libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libcairo2 \
    libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 \
    libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 \
    libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxss1 libxtst6 libappindicator1 \
    libnss3 libasound2 libatk1.0-0 libc6 ca-certificates fonts-liberation lsb-release xdg-utils \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY .  ./
ARG PIP_MIRROR_URL
RUN if [ -z "$PIP_MIRROR_URL" ] ; then pip config set global.index-url "$PIP_MIRROR_URL" ; fi

RUN pip install -e git+https://github.com/lopuhin/scrapy.git@async-def-parse#egg=Scrapy \
    -e git+https://github.com/lopuhin/scrapy-pyppeteer.git#egg=scrapy-pyppeteer \
    -e git+https://github.com/lopuhin/pyppeteer.git#egg=pyppeteer \
    -e git+https://github.com/lopuhin/scrapy-pyppeteer.git#egg=scrapy-pyppeteer \
    -r requirements.txt
RUN pip install -r requirements.txt
RUN python -c 'import pyppeteer; pyppeteer.chromium_downloader.download_chromium()'

EXPOSE 6800
CMD ["scrapyd"]