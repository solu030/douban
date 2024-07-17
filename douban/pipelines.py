# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from openpyxl.workbook import Workbook


class DoubanPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = 'Top250'
        self.ws.append(("标题","评分","主题","时长/min"))

    def close_spider(self,spider):
        self.wb.save('douban.xlsx')

    def process_item(self, item, spider):
        title = item.get('title','')
        score = item.get('score','')
        subject = item.get('subject','')
        duration = item.get('duration','')
        #append元组
        self.ws.append((title,score,subject,duration))
        return item
