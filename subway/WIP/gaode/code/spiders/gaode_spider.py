import scrapy
from scrapy.crawler import CrawlerProcess
import csv

date_code = 1657462573319 # 2022年7月10日22:16

class GaodeSpider(scrapy.Spider):
  name = 'gaode'
  allowed_domains = ['map.amap.com/subway/']
  start_urls = ['https://map.amap.com/subway/index.html']

  def parse(self, response):
    classnames = ["a.city", "a.other-city"] # Major cities are stored under a.city, minor cities are stored under a.other-city
    
    # Find City Information and store it in a CSV File
    with open('.\data\cities.csv', 'w', newline='', encoding='utf-8') as csv_file:
      headers = ['id', 'name', 'name_hanzi']
      writer = csv.writer(csv_file)
      writer.writerow(headers)

      # Parse and Find City Inforamtion
      for classname in classnames:
        cities = response.css(classname)
        city_id = cities.css("::attr(id)").extract()
        city_pinyin = cities.css("::attr(cityname)").extract()
        city_hanzi = cities.css("::text").extract()
        l = [city_id, city_pinyin, city_hanzi]

        # Write into CSV File
        for line in list(zip(*l)):
          print(line)
          writer.writerow(line)

if __name__ == '__main__':
  process = CrawlerProcess()
  process.crawl(GaodeSpider)
  process.start()