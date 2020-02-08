import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#Filter: Indie, English, Games, ordered alphabetically

class SteamSpider(CrawlSpider):
    name = 'indie_all'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['http://store.steampowered.com/search/?sort_by=Name_ASC&tags=492&category1=998&supportedlang=english']
    rules = (Rule(LinkExtractor(allow='page=(\d+)', restrict_css='.search_pagination_right'), callback='parse_page', follow=True),)

    def parse_page(self, response):
        for game in response.css('a.search_result_row'):
            yield {
                    'appid': game.css('a::attr(data-ds-appid)').get(),
                    'url': game.css('a[href*=store]::attr(href)').get(),
                    'title': game.css('span.title::text').get(),
                    'release_date': game.css('div.col.search_released.responsive_secondrow::text').get(),
                    'price': game.css('div.col.search_price.responsive_secondrow::text').get().strip(),
            }

