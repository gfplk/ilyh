from scrapy.selector import Selector
import re

XpathParser = Selector

class ReParser(object):
    def __init__(self, re_text):
        self.match = re.compile(re_text)

    def compute(self, text):
        m = self.match.search(text)
        return m.group() if m else None
