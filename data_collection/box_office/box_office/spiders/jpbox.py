import scrapy
from box_office.items import BoxOfficeItem


class JpboxSpider(scrapy.Spider):
    name = 'jpbox'
    allowed_domains = ['jpbox-office.com']
    start_urls = ['https://jpbox-office.com/v9_demarrage.php?view=2&filtre=classg&limite=0&infla=0&variable=0&tri=champ0&order=DESC&limit5=0/']

    def parse(self, response):
        table_rows = response.xpath("//table[@class='tablesmall tablesmall5']//tr")
        item = BoxOfficeItem()

        for row in table_rows :
            
            item['name'] = row.xpath(".//td[@class='col_poster_titre ']/h3/a/text()").get()
            item['entries'] = row.xpath(".//td[@class='col_poster_contenu_majeur '][1]/text()").get()

            yield item
