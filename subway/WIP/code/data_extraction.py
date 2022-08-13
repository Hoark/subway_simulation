import sys
import urllib.request
from bs4 import BeautifulSoup
import json

url_root = 'https://dt.8684.cn/'

def get_citylist():
  # Get List of City Names and URLs
  url = 'https://dt.8684.cn/'
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html,"lxml")
  cities = soup.find(attrs={"class":"li_right line"}).find_all("a")

  citylist = []
  for city in cities:
    cityinfo = {}
    cityinfo["name"] = city.text
    cityinfo["abbr"] = city["href"].split("dt.8684.cn/")[1]
    cityinfo["url"] = city["href"]
    citylist.append(cityinfo)
    
  with open('.\data\citylist.json', 'w', encoding='utf-8') as f:
    json.dump({"cities":citylist}, f, ensure_ascii=False, indent=2, sort_keys=True)
  return

def get_subwayinfo(city_id):
  city_url = url_root + city_id
  html = urllib.request.urlopen(city_url)
  soup = BeautifulSoup(html,"lxml")
  lines = soup.find_all(attrs={"class":"cm-tt"})

  

  lines_info = []
  for line in lines:
    line_name = line.text
    if "未开通" not in line_name: # 不考虑未开通的路线
      line_info = {}
      line_info["url"] = line["href"]
      line_info["uid"] = line["href"].split(city_id+'_')[1]

      line_url = url_root + line["href"]
      html = urllib.request.urlopen(line_url)
      soup = BeautifulSoup(html,"lxml")
      print(soup.find("tbody").find_all("tr"))
      

  info = {}
  info["city"] = city_id
  info["city_url"] = city_url
  info["lines"] = lines_info

  with open(f'.\data\{city_id}.json', 'w', encoding='utf-8') as f:
    json.dump(info, f, ensure_ascii=False, indent=2, sort_keys=True)
  return

if __name__ == '__main__':
  #get_citylist()
  get_subwayinfo('bj')
  
    