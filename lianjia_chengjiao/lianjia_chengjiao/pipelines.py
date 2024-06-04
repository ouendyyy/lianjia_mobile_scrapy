# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
import os
class LianjiaChengjiaoPipeline:
    def __init__(self):
        print("Current working directory:", os.getcwd())
        self.json_file  = open('data.json','wb')
        self.json_exporter = JsonItemExporter(self.json_file , ensure_ascii=False, encoding='UTF-8')
        self.json_exporter.start_exporting()

    def process_item(self, item, spider):
        self.json_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.json_exporter.finish_exporting()
        self.json_file .close()
