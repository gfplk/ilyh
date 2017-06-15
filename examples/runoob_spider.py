from ilyh.parser import ReParser, Selector
from ilyh.utils import rand_user_agent
import requests
from settings import RBMQ_SETTINGS


class Category(object):
    def category(self):
        url = 'http://www.runoob.com/'
        r = requests.get(url, headers={'user-agent': rand_user_agent()})
        r.encoding = 'utf-8'
        return r.text

    def parse_category(self, html):
        if html is None:
            raise Exception('index html is none')
        res = Selector(text=html)
        cmch = res.xpath('//div[@class="col middle-column-home"]')
        categories = []
        for ccdc in cmch.xpath('./div'):
            cat_name = ccdc.xpath('./h2/text()').extract_first().strip()
            c0 = {
                'cat_name': cat_name,
                'url': '',
                'level': 0,
                'parent_id': 0,
                'sub_categories': []
            }
            for iti in ccdc.xpath('./a'):
                cat_name = iti.xpath('./h4/text()').extract_first().strip()
                link = ''.join(
                    ['http:', iti.xpath('./@href').extract_first().strip()])
                c1 = {
                    'cat_name': cat_name,
                    'url': link,
                    'level': 1,
                    'parent_id': c0['cat_name'],
                }
                c0['sub_categories'].append(c1)

            categories.append(c0)
        return categories


class Article(object):
    def get_subject_url(self, site_id, cat_id, cat_url, su_customer):
        self.site_id = site_id
        self.cat_id = cat_id

        r = requests.get(cat_url, headers={'user-agent': rand_user_agent()})
        r.encoding = 'utf-8'
        return r.text

    def parse_subject_url(self, html):
        if html is None:
            raise Exception('article html is none')
        res = Selector(text=html)
        tops = res.xpath('//a[@target="_top"]')
        for a in tops:
            subject = a.xpath('./text()').extract_first().strip()
            link = ''.join(
                ['http://www.runoob.com', a.xpath('./@href').extract_first().strip()])
            #TODO

    def get_content(self, site_id, cat_id, subject, article_url, c_customer):
        self.site_id = site_id
        self.cat_id = cat_id
        self.article_url = article_url
        self.c_customer = c_customer
        r = requests.get(article_url, headers={'user-agent': rand_user_agent()})
        r.encoding = 'utf-8'
        return r.text

    def parse_content(self, html):
        if html is None:
            raise Exception('content html is none')
        res = Selector(text=html)
        content = res.xpath('//div[@class="article-body"]/node()').extract_first()
        #TODO
