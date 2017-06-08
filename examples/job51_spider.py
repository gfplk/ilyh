from ilyh.parser import XpathParser, ReParser
from ilyh.utils import rand_user_agent
import logging
import requests
import random
logging.basicConfig(level=logging.DEBUG)

class Job51Spider:
    TruthVisitPath = ['index', 'login'] 
    def __init__(self):
        self.visitePath = []

    def index(self):
        self.visitePath.append('index')

        url = 'http://www.51job.com/'
        headers = {
            'Host': 'www.51job.com',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': rand_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            logging.info('%r - Access Index sucessfully!' % r.status_code)
            return r.cookies
        else:
            raise Exception('%r - Access index fail.' % r.status_code)

    def login(self, user, password, requestCookie):
        self.visitePath.append('login')
        url = 'http://login.51job.com/ajax/login.php'
        formData = {
            'action': 'save',
            'from_domain': 'i',
            'lang': 'c',
            'loginname': user,
            'password': password,
            'verifycode': '',
            'isread': 'on'
        }
        headers = {
            'Host': 'login.51job.com',
            'Origin': 'http://www.51job.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': rand_user_agent(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.51job.com/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        r = requests.post(url, data=formData, headers=headers, cookies=requestCookie)
        if r.status_code == 200:
            logging.info('%r - Login successfully!' % r.status_code)
            return r.cookies
        else:
            raise Exception('%r - Login fail.' % r.status_code)

    def search(self, keyword, requestCookie):
        self.visitePath.append('search')
        url = 'http://search.51job.com/list/040000,000000,0000,00,9,99,'+keyword+',2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        headers = {
            'Host': 'search.51job.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': rand_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.51job.com/',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        r = requests.get(url, headers=headers, cookies=requestCookie)
        if r.status_code == 200:
            logging.info('%r - Search successfully!' % r.status_code)
            r.encoding = 'gbk'
            xp = XpathParser(text=r.text)
            rp = ReParser('[0-9]+')
            numJobsHtml= xp.xpath('//*[@id="resultList"]/div[1]/div[3]/text()').extract_first()
            numJobs = int(rp.compute(numJobsHtml))
            logging.info('Num Jobs: %r' % numJobs)
            jobsIdHtml = xp.xpath('//div[@class="el"]/p[@class="t1 "]')[:-1]
            for jih in jobsIdHtml:
                jobId = jih.xpath('./input/@value').extract_first()
                if jobId:
                    Job51Spider.submitJob(jobId, url, r.cookies)
        else:
            raise Exception('%r - Search fail' % r.status_code)

    @classmethod
    def submitJob(cls, jobId, referer, requestCookie):
        url = 'http://my.51job.com/my/delivery/delivery.php?rand='+str(random.random())+'&jsoncallback=jQuery18305740801100126356_1496936607495&jobid=('+jobId+'%3A0)&prd=search.51job.com&prp=01&cd=search.51job.com&cp=01&resumeid=&cvlan=&coverid=&qpostset=&elementname=delivery_jobid&deliverytype=2&deliverydomain=http%3A%2F%2Fmy.51job.com&language=c&imgpath=http%3A%2F%2Fimg02.51jobcdn.com&_=1496938008708'
        headers = {
            'Host': 'my.51job.com',
            'User-Agent': rand_user_agent(),
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': referer
        }
        r = requests.get(url, headers=headers, cookies=requestCookie)
        r.encoding = 'gbk'
        if r.status_code == 200:
            if 'deliverySuccessLayer' in r.text:
                logging.info('%r - Submit job successfully!' % r.status_code)
            else:
                logging.info('%r - Submit job fail!' % r.status_code)


if __name__ == '__main__':
    j5s = Job51Spider()
    reqc = j5s.index()
    reqs = j5s.login('15800223273', 'sc5201314', reqc)
    j5s.search('python', reqs)
