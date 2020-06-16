import json
import scrapy
from pprint import pprint

class CombatSpider(scrapy.Spider):
    name = 'post_combat'
    # allowed_domains = "https://discourse.codecombat.com/latest.json?no_definitions=true&page="
    start_urls = ["https://discourse.codecombat.com/latest.json?no_definitions=true&page={}".format(i)
                  for i in range(221)]
    download_delay = 1.5
    # start_urls = [allowed_domains + "1"]
    # start_urls = ["https://discourse.codecombat.com/latest.json?no_definitions=true&page=1"]

    def parse(self, response):

        data = json.loads(response.body)
        # pprint(data)
        topics = data['topic_list']['topics']
        for topic in topics:
            try:
                post_id = topic['id']
                next_url = ('https://discourse.codecombat.com/t/{}.json?track_visit=true&forceLoad=true').format(post_id)
                yield response.follow(next_url, callback= self.post_page)
            except:
                continue


    def post_page(self, response):
        data = json.loads(response.body)
        posts = data['post_stream']['posts']
        # pprint(posts)
        for post in posts:
            yield {
                'post_id': post['id'],
                'username': post['username'],
                'created_at': post['created_at'],
                'cooked': post['cooked'],
                'post_number': post['post_number'],
                'updated_at': post['updated_at'],
                'reply_count': post['reply_count'],
                'reply_to_post_num': post['reply_to_post_number'],
                'reads': post['reads'],
                'topic_id': post['topic_id'],
                'user_id': post['user_id'],
                'topic_slug':post['topic_slug']
            }