import sys
import urllib.request
import json

from bs4 import BeautifulSoup

def get_citylist():
  url = 'https://dt.8684.cn/'
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html,"lxml")
  cities = soup.find(attrs={"class":"li_right line"}).find_all("a")

  citylist = []
  for city in cities:
    cityinfo = {}
    cityinfo["name"] = city.text
    cityinfo["url"] = city["href"]
    citylist.append(cityinfo)
    
  with open('.\data\citylist.json', 'w', encoding='utf-8') as f:
    json.dump({"cities":citylist}, f, ensure_ascii=False, indent=2, sort_keys=True)
  return


if __name__ == '__main__':
  get_citylist()
