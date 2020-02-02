# coronavirus
2019 nCoV realtime track system based Scapy + influxdb + grafana + NLTK + Stanford CoreNLP


![](static/2020-02-02-17-13-06.png)


## Getting Started

1. Build development docker image

```bash
docker-compose build
```

2. Launch docker-compose 

```bash
docker-compose up
```

3. Tigger a Scrapy cralw task
```bash
curl http://localhost:6800/schedule.json -d project=default -d spider=ifeng
```
