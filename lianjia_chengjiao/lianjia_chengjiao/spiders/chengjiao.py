import scrapy
import json
from lianjia_chengjiao.items import HouseItem
from lianjia_chengjiao.itemloader import HouseLoader
from lianjia_chengjiao.login import Login
import re
import os

class ChengjiaoSpider(scrapy.Spider):
    name = 'chengjiao'
    allowed_domains = ['m.lianjia.com','image1.ljcdn.com']
    start_urls = ['https://m.lianjia.com/sh/chengjiao/pg1']
    def start_requests(self):
        with Login() as login:
            self.cookies = login.get_cookies()  # 获取登录后的cookies
            for url in self.start_urls:
                yield scrapy.Request(url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        script_content = response.xpath('//script[contains(., "__PRELOADED_STATE__")]/text()').get()
        preloaded_state_pattern = re.compile(r'window\.__PRELOADED_STATE__\s*=\s*({.*?});', re.DOTALL)
        preloaded_state_match = preloaded_state_pattern.search(script_content)

        if preloaded_state_match:
            preloaded_state_str = preloaded_state_match.group(1)
            preloaded_state = json.loads(preloaded_state_str)

            house_urls = preloaded_state.get('chengjiaoList', {}).get('list', [])
            for house in house_urls:
                house_url = house.get('houseUrl')
                if house_url:
                    yield scrapy.Request(response.urljoin(house_url), cookies=self.cookies, callback=self.parse_house)

            if len(house_urls) >= 30:
                current_page = int(re.search(r'pg(\d+)', response.url).group(1))
                print("现在是第{}页".format(current_page))
                next_page = current_page + 1
                next_page_url = f'https://m.lianjia.com/sh/chengjiao/pg{next_page}'
                yield scrapy.Request(next_page_url, cookies=self.cookies, callback=self.parse)

    def parse_house(self, response):
        l = HouseLoader(item=HouseItem(), response=response)
        l.add_value('url', response.url)
        l.add_xpath('title', '//title/text()')

        pictext_div = response.xpath('//div[@class="sub_mod_box house_model post_ulog"]//div[@class="pictext flexbox"]')
        if pictext_div:
            total_area = 0.0
            # 提取 data-frame 属性的值
            data_frame = pictext_div.xpath('./@data-frame').get()
            data_frame_json = json.loads(data_frame)
            for data in data_frame_json:
                total_area += float(data["area"])
            total_area = round(total_area, 2)
            l.add_value('data_frame', data_frame_json)
            l.add_value('totalArea', total_area)
            l.add_xpath('areaInTitle', '//h3[@class="house_desc"]/text()')
            l.add_xpath('transactionPrice', '//h3[@class="similar_data"]/div/p[@class="red big"]/span[@data-mark="price"]/text()')
            l.add_xpath('unitPrice', '//div[@class="similar_data_detail"]/p[@class="red big"][2]/text()')
            l.add_xpath('source', '//ul[@class="house_description big lightblack"]/li[@class="short"][1]/text()')
            l.add_xpath('transactionTime', '//ul[@class="house_description big lightblack"]/li[@class="short"][2]/text()')
            l.add_xpath('towards', '//ul[@class="house_description big lightblack"]/li[@class="short"][3]/text()')
            l.add_xpath('layer', '//ul[@class="house_description big lightblack"]/li[@class="short"][4]/text()')
            l.add_xpath('buildingType', '//ul[@class="house_description big lightblack"]/li[@class="short"][5]/text()')
            l.add_xpath('Elevator', '//ul[@class="house_description big lightblack"]/li[@class="short"][6]/text()')
            l.add_xpath('decorate', '//ul[@class="house_description big lightblack"]/li[@class="short"][7]/text()')
            l.add_xpath('generation', '//ul[@class="house_description big lightblack"]/li[@class="short"][8]/text()')
            l.add_xpath('usage', '//ul[@class="house_description big lightblack"]/li[@class="short"][9]/text()')
            l.add_xpath('ownership', '//ul[@class="house_description big lightblack"]/li[@class="short"][10]/text()')
            l.add_xpath('community', '//ul[@class="house_description big lightblack"]/li[@class="long  arrow "][1]/a/text()')

            l.add_xpath('houseType', '//ul[@class="info_ul"][1]/li[@class="info_li"][1]/p[@class="info_content deep_gray"]/text()')
            l.add_xpath('InnerArea', '//ul[@class="info_ul"][1]/li[@class="info_li"][2]/p[@class="info_content deep_gray"]/text()')
            l.add_xpath('houseStructure', '//ul[@class="info_ul"][1]/li[@class="info_li"][3]/p[@class="info_content deep_gray"]/text()')
            l.add_xpath('ratioOfElevatorResidents', '//ul[@class="info_ul"][1]/li[@class="info_li"][4]/p[@class="info_content deep_gray"]/text()')
            l.add_xpath('equippedWithElevator', '//ul[@class="info_ul"][1]/li[@class="info_li"][5]/p[@class="info_content deep_gray"]/text()')
            l.add_xpath('transactionOwnership', '//ul[@class="info_ul"][1]/li[@class="info_li"][6]/p[@class="info_content deep_gray"]/text()')
            l.add_xpath('propertyOwnership', '//ul[@class="info_ul"][1]/li[@class="info_li"][7]/p[@class="info_content deep_gray"]/text()')

            l.add_xpath('houseAge', '//ul[@class="info_ul"][2]/li[@class="info_li"][1]/p[@class="info_content deep_gray"]/text()')
            l.add_xpath('housingProposes', '//ul[@class="info_ul"][2]/li[@class="info_li"][2]/p[@class="info_content deep_gray"]/text()')
            l.add_xpath('lianjiaId', '//ul[@class="info_ul"][2]/li[@class="info_li"][5]/p[@class="info_content deep_gray"]/text()')
            image_url = response.xpath('//img[@class="lazyload"][1]/@origin-src').get()
            lianjiaId = response.xpath('//ul[@class="info_ul"][2]/li[@class="info_li"][5]/p[@class="info_content deep_gray"]/text()').get()
            if image_url:
                image_dir = "./images"
                os.makedirs(image_dir, exist_ok=True)
                img_name = f'{lianjiaId}.jpg'  # 或者根据需要生成其他的图片名称
                img_path = os.path.join(image_dir, img_name)
                yield scrapy.Request(url=image_url, callback=self.save_image, meta={'img_path': img_path, 'loader': l})
            yield l.load_item()

    def save_image(self, response):
        img_path = response.meta['img_path']
        loader = response.meta['loader']
        with open(img_path, 'wb') as f:
            f.write(response.body)
        loader.add_value('img_path', img_path)
        yield loader.load_item()
