import scrapy


class Hatla2eeSpider(scrapy.Spider):
    name = "cars"
    start_urls = [
        "https://eg.hatla2ee.com/en/car/hyundai/excel/6881376",
    ]

    def parse(self, response):
        yield {
            "title": response.xpath('//*[@id="UpperContent"]/div/div[4]/div[2]/div[1]/div/h1/text()').get(),
            "Make":  response.xpath('//*[@id="UpperContent"]/div/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/span[2]/text()').get().strip(),
            "Model": response.xpath('//*[@id="UpperContent"]/div/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/span[2]/text()').get().strip(),
            "Year": response.xpath('//*[@id="UpperContent"]/div/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div[3]/span[2]/text()').get().strip(),
            "Kms": response.xpath('//*[@id="UpperContent"]/div/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div[4]/span[2]/text()').get().strip(),
            "Transmission": response.css('#UpperContent > div > div.usedUnitWrap > div.usedUnitCarWrap > div.usedUnitCarBody > div.usedUnitCarDesc > div > div.DescDataContain > div.DescDataWrap > div > div:nth-child(5) > span.DescDataVal ::text').get().strip(),
            "Price": response.css('#UpperContent > div > div.usedUnitWrap > div.usedUnitCarWrap > div.usedUnitCarHead > div > div > span ::text').get().strip(),
            ##"Image": response.xpath('//*[@id="UpperContent"]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div/img/@data-src').extract()
            "Images": response.css(  '#UpperContent > div > div.usedUnitWrap > div.usedUnitCarWrap > '
                                     'div.usedUnitCarBody > div.usedUnitCarGallery.complete > div.usedUnitGalleryBody > '
                                     'div > div > div.swiper-wrapper > div > div.gallerySwipeImg > img.swiper-lazy::attr(data-src)').getall()
        }

        #next_page = response.css('li.next a::attr("href")').get()
        #if next_page is not None:
        #   yield response.follow(next_page, self.parse)