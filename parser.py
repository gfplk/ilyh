from scrapy.selector import Selector
import re

# xpath 解析器
XpathParser = Selector


class ReParser(object):
    '''
    正则表达式解析封装
    '''
    def __init__(self, re_text):
        self.match = re.compile(re_text)

    def compute(self, text):
        m = self.match.search(text)
        return m.group() if m else None
