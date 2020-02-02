from nltk.parse import CoreNLPParser

parser = CoreNLPParser('http://localhost:9001')
ner_tagger = CoreNLPParser(url='http://localhost:9001', tagtype='ner')
segs = list(parser.tokenize(
    u'截至1月20日24时，中国境内累计报告新型冠状病毒感染的肺炎确诊病例291例（湖北270例，北京5例，广东14例，上海2例）。'))
print(list(ner_tagger.tag(segs)))
