import requests

class Spider(object):
    def get(url, playload={}, cookies={}, headers={}, timeout=30, proxies={}):
        return requests.get(url, playload=playload, cookies=cookies, 
            headers=headers, timeout=timeout, proxies=proxies)

    def post(url, playload={}, cookies={}, headers={}, timeout=30, proxies={}, verify=False):
        return requests.post(url, playload=playload, cookies=cookies, 
            headers=headers, timeout=timeout, proxies=proxies, verify=verify)
