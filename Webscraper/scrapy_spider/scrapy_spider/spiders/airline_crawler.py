import json
import scrapy

class SpidyQuotesSpider(scrapy.Spider):
    name = 'test'
    with open('data1.json') as f:
        data = json.load(f)
    start_urls = []
    for post in data:
        start_urls.append('https://www.airlinepilot.life/t/{}.json?track_visit=true&forceLoad=true'.format(post['id']))
    download_delay = 1.5
    
    def parse(self, response):
        data = json.loads(response.body)
        posts = data['post_stream']['posts']
        for topics in posts:
            yield {
                'post_text': topics['cooked'],
                'post_id': topics['id'],
                'user_id': topics['user_id'],
                'username': topics['username'],
                'reply_to_post_num': topics['reply_to_post_number'],
                'topic_id': topics['topic_id'],
                'post_num': topics['post_number'],
                'reply_count': topics['reply_count'],
                'created at': topics['created_at'],
                'updated_at': topics['updated_at'],
                'num_reads': topics['reads'],
                'topic_slug': topics['topic_slug']
            }