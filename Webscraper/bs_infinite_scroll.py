#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Created Date: Sunday, May 31st 2020, 1:50:42 pm
# Author: Charlene Leong charleneleong84@gmail.com
# Last Modified: Sunday, May 31st 2020, 5:39:57 pm
###
"""

BeautifulSoup does not support XPath expression by default, so we use CSS
the expression here, but you can use https://github.com/scrapy/parsel to write
XPath to extract data as you like

"""
from bs4 import BeautifulSoup
import requests
from urllib import parse

START_PAGE = "https://scrapingclub.com/exercise/list_infinite_scroll/"

QUEUE = []

def parse_list_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    links = soup.select('a[class="page-link next-page"]')
    if links:
        next_link = links[0].attrs['href']
        next_link = url[:url.find('?')] + next_link
        QUEUE.append(
            (parse_list_page, next_link)
        )

    links = soup.select('div.col-lg-8 div.card a')
    for link in links:
        product_url = link.attrs['href']
        result = parse.urlparse(url)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        product_url = parse.urljoin(base_url, product_url)
        QUEUE.append(
            (parse_detail_page, product_url)
        )


def parse_detail_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    print(f"\nProcessing {url}\n")
    print(soup)

    
def main():
    """
    Push callback method and url to queue
    """
    QUEUE.append(
        (parse_list_page, START_PAGE)
    )

    while len(QUEUE):
        call_back, url = QUEUE.pop(0)
        call_back(url)

if __name__ == '__main__':
    main()