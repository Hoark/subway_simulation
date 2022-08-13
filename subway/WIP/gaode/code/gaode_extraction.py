import sys
import urllib.request
import json
import os
import csv

def main(cid, cname, dateID, dateYYYYMMDD):
  # Create folder
  folderpath = f'.\data\{cid}'
  if not os.path.exists(folderpath):
    os.makedirs(folderpath)

  # Subway Lines
  url_drw = f'http://map.amap.com/service/subway?_{dateID}&srhdata={cid}_drw_{cname}.json'
  html_drw = urllib.request.urlopen(url_drw)
  json_drw = json.loads(html_drw.read().decode("utf-8"))
  with open(f'{folderpath}\drw_{dateYYYYMMDD}.json', 'w', encoding='utf-8') as f:
    json.dump(json_drw, f, ensure_ascii=False, indent=2, sort_keys=True)

  # Time-Table
  url_info = f'http://map.amap.com/service/subway?_{dateID}&srhdata={cid}_info_{cname}.json'
  html_info = urllib.request.urlopen(url_info)
  json_info = json.loads(html_info.read().decode("utf-8"))
  with open(f'{folderpath}\info_{dateYYYYMMDD}.json', 'w', encoding='utf-8') as f:
    json.dump(json_info, f, ensure_ascii=False, indent=2, sort_keys=True)
  return

if __name__ == '__main__':
  print("~~~Start GaoDe Extraction")
  cid = sys.argv[1]
  dateID = sys.argv[2]
  dateYYYYMMDD = sys.argv[3]
  
  with open('.\data\cities.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    line_count = 0

    for row in reader:
      if line_count==0:
        headers = row
      else:
        if cid != '0000':
          # Find specific city
          if row[0] == cid:
            cname = row[1]
            main(cid, cname, dateID, dateYYYYMMDD)
        else:
          #Run through ALL cities
          city_id = row[0]
          cname = row[1]
          main(city_id, cname, dateID, dateYYYYMMDD)
      line_count += 1

  print("~~~Finished GaoDe Extraction")