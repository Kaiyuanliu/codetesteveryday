# -*- coding: utf-8 -*-
"""
一个HTML文件，找出里面的链接
find all link from a html
"""
import requests
from urlparse import urlsplit, urljoin
import re
from bs4 import BeautifulSoup

SUCCESS_STATUS_CODE = 200
SCHEME_ALLOWED = ['https', 'http']


class HTMLParse(object):

    def __init__(self, method="bs", **kwargs):
        self._method = method
        if 'path' in kwargs:
            self._url = ''
            if 'base_url' in kwargs:
                self._url = self._get_correct_url(kwargs['base_url'])
            self._html_content = self.read_html_from_file(path=kwargs['path'])
        elif 'url' in kwargs:
            self._url = self._get_correct_url(kwargs['url'])
            self._html_content = self.read_html_from_url(url=self._url)
        else:
            raise NotImplemented("please provide website url or html file directory")

    def _get_correct_url(self, url):
        return url if urlsplit(url).scheme else 'http://{url}'.format(url=url)

    def read_html_from_file(self, path):
        with open(path, "r") as f:
            return f.read().strip()

    def read_html_from_url(self, url):
        r = requests.get(url)
        if r.status_code == SUCCESS_STATUS_CODE:
            return r.content
        else:
            return ''

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    def get_all_links_from_html(self, method=None):
        self._method = method if method else self._method
        result = getattr(self, '_get_all_links_from_html_by_'+self._method, None)
        if result:
            list_result = result(html=self._html_content)
            self.filter_urls(list_result)
            return list_result
        else:
            return []

    def _get_all_links_from_html_by_bs(self, html):
        soup = BeautifulSoup(self._html_content)
        seen = set()
        seen_add = seen.add
        return [a_tag["href"] for a_tag in soup.body.findAll("a", href=True)
                if not (a_tag['href'] in seen or seen_add(a_tag['href']))]

    def _get_all_links_from_html_by_re(self, html):
        raise NotImplemented("not implemented, use beautifulsoup method instead")

    def filter_urls(self, url_list):
        for i in range(len(url_list)-1, -1, -1):
            one_url = url_list[i]
            if not urlsplit(one_url).scheme:
                url_joined = urljoin(self._url, one_url)
                if url_joined == one_url:
                    del url_list[i]
                else:
                    url_list[i] = url_joined
            elif urlsplit(one_url).scheme not in SCHEME_ALLOWED:
                del url_list[i]

    def write_result_to_file(self, result, path="result.txt"):
        with open(path, "wb") as f:
            for one in result:
                f.write(one+"\n")

if __name__ == "__main__":
    # settings = {
    #     'path': 'url_content.txt'
    # }
    settings = {
        'url': 'www.google.com'
    }
    html_parse = HTMLParse(method="re", **settings)
    result = html_parse.get_all_links_from_html()
    html_parse.write_result_to_file(result)
