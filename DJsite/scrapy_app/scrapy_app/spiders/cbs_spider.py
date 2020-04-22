import scrapy
from html.parser import HTMLParser
from ..items import CBS_item


class CBS_spider(scrapy.Spider):
    name = 'cbs_content'
    start_urls = ['https://www.cbssports.com']

    def parse(self, response):
        menu_links = self.parse_menu_links(response)
        for link in menu_links:
            if link.startswith('/'):
                if link.endswith('/'):
                    for page_number in range(1, 2, 1):
                        request = response.follow(link + str(page_number), callback=self.parse_news_links)
                        request.meta['menu_link'] = link
                        yield request

    def parse_news_links(self, response):
        menu_link = response.meta['menu_link']
        form_menu_link = menu_link.replace('/', '')
        links = response.xpath("//h5[contains(@class,'article-list-pack-title col-4')]//@href").getall()
        titles = response.xpath("//h5[contains(@class,'article-list-pack-title col-4')]//a/text()").getall()
        images = response.xpath("//div[contains(@class,'article-list-pack-image')]//img").getall()
        authors = response.xpath("//h6[contains(@class,'article-list-pack-byline')]/text()|"
                                 "//h6[contains(@class,'article-list-pack-byline')]//a/text()").getall()
        number_of_link = 0
        for link in links:
            if form_menu_link in link.split('/'):
                request = response.follow(link, callback=self.parse_content)
                request.meta['menu_link'] = form_menu_link
                request.meta['link'] = link
                request.meta['author'] = authors[number_of_link]
                request.meta['image'] = images[number_of_link]
                request.meta['title'] = titles[number_of_link]
                yield request
                number_of_link += 1

    def parse_content(self, response):
        items = CBS_item()
        title = response.meta['title']
        menu_link = response.meta['menu_link']
        link = response.meta['link']
        author = response.meta['author']
        image = response.meta['image']
        body = response.xpath("//div[@id='article-main-body']//p|"
                              "//div[@id='article-main-body']//ul|"
                              "//div[@id='article-main-body']//h3|"
                              "//div[@id='article-main-body']//img|"
                              "//div[contains(@class,'MediaShortcodeYouTubeVideo-content media-embed__content-wrapper')]").getall()
        long_title = response.xpath("//h1[contains(@class,'article-headline')]/text()").get()
        article = list()
        article = article + body
        parser = MyHTMLParser()
        parser.feed(image)
        form_image = parser.d
        items['title'] = title
        items['link'] = link
        items['menu_link'] = menu_link
        items['author'] = author
        items['image'] = form_image
        items['body'] = article
        items['tags'] = []
        items['tags'].appemd(menu_link)
        items['long_title'] = long_title
        yield items

    def parse_menu_links(self, response):
        sport_category_menu = response.xpath("//div[contains(@class,'site-nav-logo')]//@href").getall()
        return sport_category_menu


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.d = {}
        for attr in attrs:
            self.d[attr[0]] = attr[1]
