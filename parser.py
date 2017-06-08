from scrapy.selector import Selector
import re

class XpathParser(Selector):
    def __init__(self, text):
        super().__init__(text=text)

class ReParser(object):
    def __init__(self, re_text):
        self.match = re.compile(re_text)

    def compute(self, text):
        m = self.match.search(text)
        return m.group() if m else None
