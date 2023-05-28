import re

import scrapy

from pep_parse.items import PepParseItem

PEP_PATTERN = re.compile(r"^PEP\s(?P<number>\d+)[\s–]+(?P<name>.*)")


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        index = response.css("#numerical-index tbody")
        all_hrefs = index.css("a::attr(href)").getall()
        for href in all_hrefs:
            yield response.follow(href, callback=self.parse_pep)

    def parse_pep(self, response):
        pep = response.css("#pep-content")
        h1_tag = PEP_PATTERN.search(pep.css("h1::text").get())
        if h1_tag:
            number, name = h1_tag.group("number", "name")
            context = {
                'number': number,
                'name': name,
                'status': pep.css("dt:contains('Status') + dd::text").get()
            }
            yield PepParseItem(context)
