import scrapy
import json
import csv

# main_url = 'https://discourse.codecombat.com/latest?no_definitions=true&page=1'

class CombatSpider(scrapy.Spider):
    name = 'combat'
    # allowed_domains = "https://discourse.codecombat.com/latest.json?no_definitions=true&page="
    start_urls = ["https://discourse.codecombat.com/latest.json?no_definitions=true&page={}".format(i)
                  for i in range(221)]
    download_delay = 2.5
    # start_urls = [allowed_domains + "1"]
    # def start_requests(self):
    #     with open(self.settings["PROXY_CSV_FILE"], mode="r") as csv_file:
    #         requests=

    def parse(self, response):

        data = json.loads(response.body)
        # pprint(data)
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


