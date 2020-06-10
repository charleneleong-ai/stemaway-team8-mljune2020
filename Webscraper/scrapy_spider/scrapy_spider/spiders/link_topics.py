import scrapy
import json

class SpidyQuotesSpider(scrapy.Spider):
    name = 'main'
    start_urls = []
    for i in range(173):
        start_urls.append('https://www.airlinepilot.life/latest.json?no_definitions=true&page={}'.format(i+1))
    download_delay = 1.5

    def parse(self, response):
        data = json.loads(response.body)
        topics = data['topic_list']['topics']
        for topic in topics:
            yield {
                'id': topic['id'],
                'title': topic['title'],
                'created_at': topic['created_at'],
                'last_posted_at': topic['last_posted_at'],
                'views': topic['views'],
                'like_count': topic['like_count'],
                'category_id': topic['category_id']
            }