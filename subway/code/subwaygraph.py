import networkx as nx
import matplotlib.pyplot as plt

def createSubwayGraph(subwayinfo):
  G = nx.Graph()

  for line in subwayinfo["subways"]["l"]:
    cl = line['l_xmlattr']['lc'] # Colour of Line
    ln = line["l_xmlattr"]["lb"] # Line Name
    luid1 = line["l_xmlattr"]["uid"]
    luid2 = line["l_xmlattr"]["uid2"]
    isloop = line["l_xmlattr"]["loop"]

    st_prev = []
    st_count = 0
    for st in line['p']:
      if st["p_xmlattr"]["st"] and st["p_xmlattr"]["lb"]!='': # Not a Ghost Station
        name = st["p_xmlattr"]["lb"] # 站点名称
        # uid = st["p_xmlattr"]["uid"]
        pos = (st["p_xmlattr"]['x'],st["p_xmlattr"]['y']) # 站点坐标位置
        end = (st_count==0 or st_count==len(line["p"]))

        if name in G.nodes: # Station node already exists in G
          G.nodes[name]["lines"].extend([luid1,luid2])
          #G.nodes[name]["uids"].append(uid)
        else: # Need to create a station node
          '''
          站点结构包括以下变量：站点名称(key)、相连路线、坐标位置、
            在本站点候车的乘客
          '''
          G.add_node(name, lines=[luid1,luid2], pos=pos, passengers=[])

        # Time Calc
        if "info" in st["p_xmlattr"]:
          G.nodes[name]["info"] = st["p_xmlattr"]["info"]
          if st_prev: # list is not empty
            info1 = G.nodes[name]["info"]
            info2 = G.nodes[st_prev[0]]["info"]

            time = calcTime(info1, info2)     
          
            n_curr = name
            T = time / len(st_prev)
            while st_prev:
                n_prev = st_prev.pop()
                
                G.add_edge(n_curr, n_prev, time_cost=T)
                n_curr = n_prev
          
        st_prev.append(name)
        st_count += 1

    if line['l_xmlattr']['loop']: # Line is a Loop
      st1 = None; st2 = None
      for st in line['p']:
        if st["p_xmlattr"]["st"]: # Not a Ghost Station
          if st1 is None:
            st1 = st
          else:
            st2 = st
            break

      info1 = st1["p_xmlattr"]["info"]
      info2 = st2["p_xmlattr"]["info"]
      T = calcTime(info1, info2)
      T = min(10,T)
      G.add_edge(st1["p_xmlattr"]["lb"], st2["p_xmlattr"]["lb"], line=ln, time_cost=T, cd=1)
  return G

def calcTime(info1, info2):
  #find smallest time
  time = 999
  for item1 in info1:
    for item2 in info2:
      if item1["uid"] == item2["uid"]: # Same Line
        for timetype in ["first_time", "last_time"]:
          if item1[timetype]!='' and item2[timetype]!='':
            t1 = int(item1[timetype].split(':')[0])*60 + int(item1[timetype].split(':')[1])
            t2 = int(item2[timetype].split(':')[0])*60 + int(item2[timetype].split(':')[1])
            t = abs(t1-t2)
            time = min(t,time)     
  if time==999:
    time = 30
  return time

def drawGraph(G):
  labels = nx.get_node_attributes(G, 'n') 
  positions = nx.get_node_attributes(G, 'pos')
  nx.draw(G, with_labels=True, font_family='SimHei', pos=positions)
  plt.gca().invert_yaxis()
  plt.show()
  return

def shortest_path(G, source, target):
  path = nx.shortest_path(G, source, target, weight="time_cost")
  length = nx.shortest_path_length(G, source, target, weight="time_cost")
  # print(path)
  # print(f"时间：{round(length)}分钟 | 途径：{len(path)}站")
  return (path, round(length))