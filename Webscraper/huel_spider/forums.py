import scrapy 
from scrapy.crawler import CrawlerProcess
import json 
import csv
import html2text

class ForumSpider(scrapy.Spider):
    name = 'forum'
    download_delay = 2.5
    base_url = 'https://discourse.huel.com/latest.json?no_definitions=true&page='
    end = 0
    next_page = ''
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36' 
    }

    def __init__(self):
        with open('huel.csv', 'w') as csv_file:
            csv_file.write('post_text, post_id, user_id, username, reply_to_post_num, topic_id, post_num, reply_count, created_at, updated_at, num_reads, topic_slug, forum_name\n')

    def start_requests(self):
        next_page = self.base_url + str(self.end)
        yield scrapy.Request(url = next_page, headers = self.headers, callback = self.parse)

    def parse(self, response):
            data = json.loads(response.text)
            #data extraction
            for posts in data['topic_list']['topics']: 
                NewLink = 'https://discourse.huel.com/t/' + str(posts['id']) + '.json?track_visit=true&forceLoad=true' 
                yield scrapy.Request(NewLink, headers = self.headers, callback = self.parse_ind)
            if len(data['topic_list']['topics']) > 0:
                self.end = self.end + 1
                yield scrapy.Request(self.base_url + str(self.end), headers = self.headers, callback = self.parse)
            
    def parse_ind(self, response):
        text = json.loads(response.text)
        h = html2text.HTML2Text()
        h.unicode_snob = False
        #pullling out individual data
        for info in text['post_stream']['posts']:
            information = {
                'post_text' : h.handle(info['cooked']).replace('\n', ' ').replace('  ', ' '),
                'post_id' : info['id'],
                'user_id' : info['user_id'],
                'username' : info['username'],
                'reply_to_post_num' : info['reply_to_post_number'],
                'topic_id' : info['topic_id'],
                'post_num' : info['post_number'],
                'reply_count' : info['reply_count'],
                'created_at' : info['created_at'],
                'updated_at' : info['updated_at'],
                'num_reads' : info['readers_count'],
                'topic_slug' : info['topic_slug'],
                'forum_name' : "huel"
            }
            print(json.dumps(information, indent = 2))
            print(self.end)
            with open('huel.csv', 'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames= information.keys())
                writer.writerow(information)


process = CrawlerProcess()
process.crawl(ForumSpider)
process.start()

