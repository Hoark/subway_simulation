import sys
import urllib.request
import json

def extract_citylist():
  print("~~~Start Citylist Data Extraction")

  url = 'http://map.baidu.com/?qt=subwayscity'
  html = urllib.request.urlopen(url)
  json_r = json.loads(html.read().decode("utf-8"))
  with open('data\citylist.json', 'w', encoding='utf-8') as f:
    json.dump(json_r, f, ensure_ascii=False, indent=2, sort_keys=True)

  print("~~~Finish Citylist Data Extraction")
  return

def extract_city(code):
  print(f"~~~Start Data Extraction for {code}")

  # Subway Lines
  url = f'https://map.baidu.com/?qt=subways&c={code}&format=json'
  html = urllib.request.urlopen(url)
  json_r = json.loads(html.read().decode("utf-8"))
  
  # Info
  for line in json_r['subways']['l']:
    for st in line["p"]:
      if st["p_xmlattr"]["st"]: # Not a Ghost Station
        if "uid" in st["p_xmlattr"]: # Station has a UID
          uid = st["p_xmlattr"]["uid"]
          url = f'https://map.baidu.com/?qt=inf&uid={uid}'
          html = urllib.request.urlopen(url)
          st_info = json.loads(html.read().decode("utf-8"))['content']['ext']['line_info']
          st["p_xmlattr"]["info"] = st_info

          print(st["p_xmlattr"]["lb"] + "--成功")
        else:
          print(st["p_xmlattr"]["lb"] + "--失败")

  with open(f'data\{code}.json', 'w', encoding='utf-8') as f:
    json.dump(json_r, f, ensure_ascii=False, indent=2, sort_keys=True)

  print(f"~~~Finish Data Extraction for {code}")
  return

if __name__ == '__main__':
  if sys.argv[1] == 'True':
    # Extract City List
    extract_citylist()
  if sys.argv[2] != '-1':
    # Extract City Data
    if sys.argv[2] == '0':
      # Extract All Cities
      citylist = json.load(open('data\citylist.json', 'r', encoding='utf-8'))
      for city in citylist['subways_city']['cities']:
        code = city['code']
        extract_city(code)
    else:
      # Extract One City
      extract_city(sys.argv[2])




    
    