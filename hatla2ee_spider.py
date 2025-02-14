import scrapy

_selector = '#listCar-container > div.CarListWrapper > div > div > div.newCarListUnit_data_wrap > div.newCarListUnit_data_contain > div.newCarListUnit_header > span'
_root_url = 'https://eg.hatla2ee.com/en/car/search'


def numerical_value(text, unit):
    if not text or not unit:
        return None
    try:
        value = float(text.replace(unit, '').replace(',', ''))
        return value
    except ValueError:
        return None


class Hatla2eeSpider(scrapy.Spider):
    name = "cars"
    default_url = "https://eg.hatla2ee.com/en/car/search?make=12&model=35&city=0&body=&transmission=0&fuel=&priceMin=&priceMax=&kmMin=&kmMax=&dateMin=0&dateMax=0&color=&accountMin=&accountMax=&installmentMin=&installmentMax="


    def __init__(self, full_url, **kwargs):
        super().__init__(**kwargs)
        print('full_url: {}'.format(full_url))
        if not full_url:
            self.full_url = self.default_url
        elif full_url and full_url.startswith(_root_url):
            self.full_url = full_url
        else:
            raise ValueError('URL must start with {}'.format(_root_url))

        self.start_urls = [
            full_url,
            f"{full_url}&page=2",
            f"{full_url}&page=3"
            # Add more pages as needed...
        ]
        print(self.full_url)


    def parse(self, response):
        for car in response.css(_selector):
            # title = car.css('a::text').get(),
            #yield {'title': car.css('a::text').get()}
            absolute_url =  response.urljoin(car.css('a::attr(href)').get())
            yield scrapy.Request(url=absolute_url, callback=self.parse_details)

    def parse_details(self, response):



        self.div_used_unit_car_wrap = response.css('#UpperContent > div > div.usedUnitWrap > div.usedUnitCarWrap')
        self.div_used_unit_car_head = self.div_used_unit_car_wrap.css('div.usedUnitCarHead')
        self.div_used_unit_car_body = self.div_used_unit_car_wrap.css('div.usedUnitCarBody')
        self.div_desc_data_wrap = self.div_used_unit_car_body.css('div.usedUnitCarDesc > div > div.DescDataContain > div.DescDataWrap')

        title = self.div_used_unit_car_head.css('div > h1 ::text').get().strip()
        make = self.div_desc_data_wrap.css('div > div:nth-child(1) > span.DescDataVal ::text').get().strip()
        model = self.div_desc_data_wrap.css('div > div:nth-child(2) > span.DescDataVal ::text').get().strip()
        year = self.div_desc_data_wrap.css('div > div:nth-child(3) > span.DescDataVal ::text').get().strip()
        mileage = self.div_desc_data_wrap.css('div > div:nth-child(4) > span.DescDataVal ::text').get().strip()
        transmission = self.div_desc_data_wrap.css('div > div:nth-child(5) > span.DescDataVal ::text').get().strip()
        city = self.div_desc_data_wrap.css('div > div:nth-child(6) > span.DescDataVal ::text').get().strip()
        color = self.div_desc_data_wrap.css('div > div:nth-child(7) > span.DescDataVal ::text').get().strip()
        price = self.div_used_unit_car_head.css('div > div > span ::text').get().strip()
        image = response.xpath('//*[@id="UpperContent"]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div/img/@data-src').get()

        yield {
            "title":title,
            "Make":make,
            "Model":model,
            "Year": year,
            "mileage": mileage,
            "Transmission": transmission,
            "City": city,
            "Color": color,
            "Price": price,
            "Image": '=IMAGE("{}")'.format(image),
            "mileage_numerical": numerical_value(mileage, 'Km'),
            "price_numerical": numerical_value(price, "EGP")
        }
