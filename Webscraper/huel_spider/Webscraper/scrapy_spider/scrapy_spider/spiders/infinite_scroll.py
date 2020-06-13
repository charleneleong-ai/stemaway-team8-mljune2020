#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Created Date: Sunday, May 31st 2020, 1:23:21 pm
# Author: Charlene Leong charleneleong84@gmail.com
# Last Modified: Sunday, May 31st 2020, 3:58:59 pm
###

import json
import logging

import scrapy
from scrapy.http.request import Request

from six.moves.urllib import parse

class List_infinite_scroll_Spider(scrapy.Spider):
    name = "infinite_scroll"

    def start_requests(self):
        yield Request(
            url="https://scrapingclub.com/exercise/list_infinite_scroll/",
            callback=self.parse_list_page
        )

    def parse_list_page(self, response):
        """
        The url of next page is like
        https://scrapingclub.com/exercise/list_infinite_scroll/?page=2

        It can be found in a.next-page
        """
        #First, check if next page available, if found, yield request
        next_link = response.xpath(
            "//a[@class='page-link next-page']/@href").extract_first()
        if next_link:
            # If the website has strict policy, you should do more work here
            # Such as modifying HTTP headers

            # concatenate url
            url = response.url
            next_link = url[:url.find('?')] + next_link
            yield Request(
                url=next_link,
                callback=self.parse_list_page
            )

        # find product link and yield request back
        for req in self.extract_product(response):
            yield req

    def extract_product(self, response):
        links = response.xpath("//div[@class='col-lg-8']//div[@class='card']/a/@href").extract()
        for url in links:
            result = parse.urlparse(response.url)
            base_url = parse.urlunparse(
                (result.scheme, result.netloc, "", "", "", "")
            )
            url = parse.urljoin(base_url, url)
            yield Request(
                url=url,
                callback=self.parse_product_page
            )

    def parse_product_page(self, response):
        """
        The product page use ajax to get the data, try to analyze it and finish it
        by yourself.
        """
        logging.info("processing " + response.url)
        
        
        yield None