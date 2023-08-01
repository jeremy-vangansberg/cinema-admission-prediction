import scrapy
from box_office.items import BoxOfficeItem


class JpboxSpider(scrapy.Spider):
    name = 'spider_jpbox'
    allowed_domains = ['jpbox-office.com']
    start_urls = [
        'https://jpbox-office.com/v9_demarrage.php?view=2&filtre=classg&limite=0&infla=0&variable=0&tri=champ0&order=DESC&limit5=0/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'box_office.pipelines.BoxOfficePipeline': 300,
            'box_office.pipelines.SaveAzureSQLPipeline': 400,
        },
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, meta={'limit': 0})

    def parse(self, response):
        movies_links_list = response.xpath(
            "//table[@class='tablesmall tablesmall5']//tr//h3/a/@href").getall()

        for movie_link in movies_links_list:
            absolute_movie_link = response.urljoin(movie_link)
            yield scrapy.Request(url=absolute_movie_link, callback=self.parse_movie)

        limit = response.meta['limit'] + 30

        if limit < 9330:
            next_page_url = f'https://jpbox-office.com/v9_demarrage.php?view=2&filtre=classg&limite={limit}&infla=0&variable=0&tri=champ0&order=DESC&limit5=0'
            yield scrapy.Request(url=next_page_url, callback=self.parse, meta={'limit': limit})

    def parse_movie(self, response):
        item = BoxOfficeItem()
        item['title'] = response.xpath("//h1/text()").get()
        item['original_title'] = response.xpath("//h2/text()").get()
        item['director'] = response.xpath("(//table)[2]//h4/a/text()").get()
        item['release_date'] = response.xpath(
            "//div[@class='bloc_infos_center tablesmall1b']//a/text()").get()
        item['entries'] = response.xpath(
            "//table[@class='tablesmall tablesmall2']//tr[last()]//td[@class='col_poster_contenu_majeur']/text()").get()
        item['duration'] = response.xpath(
            "((//table)[2]//h3//text())[5]").getall()

        yield item
