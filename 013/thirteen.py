# -*- coding: utf-8 -*-

import os
import re
import requests
from urlparse import urlsplit

DEFAULT_URL = "http://tieba.baidu.com/p/2166231880"
SUCCESS_STATUS_CODE = 200


class ImageSpiderCrawling(object):

    """
    initialize parameters
    @param url: the url that will be crawling
    """
    def __init__(self, url=DEFAULT_URL):
        self._url = url
        self._r = None

    """
    load url by using requests
    @param url: the url that will be crawling
    @param parameter: url parameters
    @param returned: True: will return the url, False: otherwise
    """
    def load_url(self, url="", parameter="", returned=False):
        self._url = url if url else self._url
        url_netloc = urlsplit(self._url)[1]
        if url_netloc == urlsplit(DEFAULT_URL)[1]:
            self._url = self._url + '?see_lz=1'
        parameter = '&'+parameter if parameter else parameter
        self._url = self._url + parameter
        self._r = requests.get(self._url)
        if returned:
            return self._url

    """
    get total number pages from a url
    @param url: the url that will be crawling
    @return: the total number pages
    """
    def get_page(self, url=""):
        if self._r is None:
            self.load_url(url)
        total_page = 0
        if self._r.status_code == SUCCESS_STATUS_CODE:
            url_content = self._r.content
            total_number_re = '<span class="red">(.*?)</span>'
            pages = re.findall(total_number_re, url_content)
            total_page = pages[0]
        self._r = None
        return total_page

    """
    download images from a page
    @param page: which page will be used for crawling images
    """
    def download_images(self, page):
        self.load_url(parameter="pn="+str(page))
        if self._r.status_code == SUCCESS_STATUS_CODE:
            url_content = self._r.content
            img_urls_re = 'img .*?class="BDE_Image" src="(.*?)"'
            img_urls = re.findall(img_urls_re, url_content)
            self._r = None
            self.write_images(img_urls)

    """
    write images to local directory
    @param img_urls: a list that contains all the image urls
    @param output_path: the images saving path
    """
    def write_images(self, img_urls, output_path=os.getcwd()):
        for img_url in img_urls:
            self.load_url(img_url)
            if self._r.status_code == SUCCESS_STATUS_CODE:
                image_name = os.path.basename(urlsplit(img_url).path)
                image_path = os.path.join(output_path, image_name)
                with open(image_path, "wb") as f:
                    f.write(self._r.content)
        self._r = None


if __name__ == "__main__":
    image_spider_crawling = ImageSpiderCrawling()
    total_pages = image_spider_crawling.get_page()
    for page in total_pages:
        image_spider_crawling.download_images(page)
