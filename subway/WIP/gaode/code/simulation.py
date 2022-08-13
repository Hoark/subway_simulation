from cProfile import label
import sys
import json
import networkx as nx
import matplotlib.pyplot as plt

def createSubwayGraph(drwjson, infojson):
  G = nx.Graph()

  for line in drwjson['l']:
    cl = line['cl'] # Colour of Line

    sid_prev = None
    for station in line['st']:
      sid_curr = station['sid']

      # Add attributes to Node
      G.add_node(sid_curr, n=station['n']) # 站点名称（汉子）
      G.add_node(sid_curr, npy=station['sp']) # 站点名称（拼音）

      # Add edge
      if sid_prev is not None and sid_curr is not None:
        G.add_edge(sid_prev, sid_curr, color=cl)

      sid_prev = sid_curr
      
  return G

def drawGraph(G):
  labels = nx.get_node_attributes(G, 'n') 
  nx.draw(G, labels=labels, font_family='SimHei')
  plt.show()
  return

if __name__ == '__main__':
  print('~~~Start Simulation')
  cid = sys.argv[1]
  dateYYYYMMDD = sys.argv[2]

  drwjson = json.load(open(f'./data/{cid}/drw_{dateYYYYMMDD}.json', 'r', encoding='utf-8'))
  infojson = json.load(open(f'./data/{cid}/info_{dateYYYYMMDD}.json', 'r', encoding='utf-8'))

  G = createSubwayGraph(drwjson, infojson)

  drawGraph(G)

  print('~~~Finish Simulation')