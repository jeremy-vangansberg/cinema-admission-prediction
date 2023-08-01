import scrapy
from box_office.items import BoxOfficeItem, FeaturesItem
import re


class FeaturesSpider(scrapy.Spider):
    name = 'soon_release'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/film/agenda']

    custom_settings = {
        'ITEM_PIPELINES': {
            'box_office.pipelines.FeaturesPipeline': 300,
            'box_office.pipelines.SoonReleaseSaveAzureSQLPipeline': 400,
        },
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        movies_links_list = response.xpath(
            "//h2/a/@href").getall()

        for movie_link in movies_links_list:
            absolute_movie_link = 'https://www.allocine.fr' + movie_link
            yield scrapy.Request(url=absolute_movie_link, callback=self.parse_movie)

    def parse_movie(self, response):
        item = FeaturesItem()
        item['title'] = response.xpath("//h1/text()").get()

        item['director'] = response.xpath(
            "(//div[@class='meta-body-item meta-body-direction'])[1]/span[last()]/text()").get()

        item['actors'] = response.xpath(
            "(//div[@class='meta-body-item meta-body-actor'])[1]//span/text()").getall()

        item['id_film'] = re.findall(r'(\d+)', response.url)[0]

        item['synopsis'] = response.xpath(
            "(//div[@class='content-txt '])/text()").getall()

        item['release_date'] = response.xpath(
            "(//div[@class='meta-body-item meta-body-info'])/span[1]/text()").get()

        item['duration'] = response.xpath(
            "(//div[@class='meta-body-item meta-body-info'])/text()").getall()

        item['genre'] = response.xpath(
            "//div[@class='meta-body-item meta-body-info']/span/text()").getall()

        item['language'] = response.xpath(
            "//span[contains(preceding-sibling::span[1]/text(), 'Langues')]/text()").get()

        item['country'] = response.xpath(
            "//span[contains(@class, 'nationality')]/text()").get()

        item['original_title'] = response.xpath(
            "//div[contains(span/text(), 'Titre original ')]/text()[2]").get()

        item['distrib'] = response.xpath(
            "//span[contains(preceding-sibling::span[1]/text(), 'Distributeur')]/text()").get()

        yield item
