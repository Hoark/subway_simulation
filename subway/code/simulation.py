import sys
import json
from random import randint
import os

from subwaygraph import createSubwayGraph, shortest_path
from utils import nextID, time_str2int, time_int2str

# Globals
lines = {}
passengers = {}; pid = "p0000000"
trains = {}; tid = "t0000000"

def createLines(subwayinfo):
  for line in subwayinfo["subways"]["l"]:
    l = {}
    ln = line["l_xmlattr"]["lb"] # Line Name
    luid = (line["l_xmlattr"]["uid"], line["l_xmlattr"]["uid2"])
    loop = line["l_xmlattr"]["loop"]
    path = []
    for st in line["p"]:
      if st["p_xmlattr"]["st"] and st["p_xmlattr"]["lb"]!='':
        path.append(st["p_xmlattr"]["lb"])
    
   
    if not loop:
      terminals = ((path[0],0),(path[-1],0))
    else:
      terminals = ((path[0],0),(path[1],0))
    
    l["terminals"] = terminals
    l["path"] = path
    l["loop"] = loop
    l["luid"] = luid

    lines[ln] = l

  return

def newPassengers(G,time):
  # 生成新的乘客
  st_list = list(G.nodes) # List of Station Names
  global passengers, pid
  
  # 每一站点生成一个随机乘客（随机目的地）
  for st in st_list:
    p = {}
    p["source"] = st

    target = st
    while target == st:
      target = st_list[randint(0,len(st_list)-1)]
    p["target"] = target # Random target

    (p["path"], p["estimated_time"]) = shortest_path(G, p["source"], p["target"])
    p["start_time"] = time_int2str(time)
    p["end_time"] = ''
    del p["path"][0]
    p["next_station"] = p["path"][0]
    p["time2station"] = 0
    p["status"] = "候车" #0: 已到达，1：乘车，2：候车
    p["log"] = []
    passengers[pid] = p
    G.nodes[st]["passengers"].append(pid)
    pid = nextID(pid)
  return

def newTrains(G, time):
  # 生成新的列车
  global lines, trains, tid

  for ln in lines:
    line = lines[ln]
    loop = line["loop"]
    [(t1,cd1), (t2,cd2)] = line["terminals"]

    # To-do: 环路
    if not loop:
      if cd1<=0:
        for item in G.nodes[t1]["info"]:
          if item["terminals"]==t2:
            if time>=time_str2int(item["first_time"]) and time<=time_str2int(item["last_time"]):
              train1 = {}
              path = line["path"].copy()
              
              train1["source"] = t1
              train1["line"] = ln
              train1["loop"] = loop
              train1["path"] = path
              train1["next_station"] = path[0]
              train1["time2next"] = 0
              train1["passengers"] = []
              trains[tid] = train1
              tid = nextID(tid)
              cd1 = 5

      else:
        cd1 -= 1
    
      if cd2<=0:
        for item in G.nodes[t2]["info"]:
          if item["terminals"]==t1:
            if time>=time_str2int(item["first_time"]) and time<=time_str2int(item["last_time"]):
              train2 = {}
              path = list(reversed(line["path"]))
              
              train2["source"] = t2
              train2["line"] = ln
              train2["loop"] = loop
              train2["path"] = path
              train2["next_station"] = path[0]
              train2["time2next"] = 0
              train2["passengers"] = []
              trains[tid] = train2
              tid = nextID(tid)
              cd2 = 5
      else:
        cd2 -= 1

      line["terminals"] = [(t1,cd1), (t2,cd2)]
      lines[ln] = line

    else: # Loop
      if cd1<=0:
        for item in G.nodes[t1]["info"]:
          if item["terminals"]==t1 and item["line_name"]==ln:
            if time>=time_str2int(item["first_time"]) and time<=time_str2int(item["last_time"]):
              train1 = {}
              idx = line["path"].index(t1)
              path = line["path"][idx::] + line["path"][:idx:]
              
              train1["source"] = t1
              train1["line"] = ln
              train2["loop"] = loop
              train1["path"] = path
              train1["next_station"] = path[0]
              train1["time2next"] = 0
              train1["passengers"] = []
              trains[tid] = train1
              tid = nextID(tid)
              cd1 = 5

              train2 = {}
              path = list(reversed(path))
              
              train2["source"] = t2
              train2["line"] = ln
              train2["loop"] = loop
              train2["path"] = path
              train2["next_station"] = path[0]
              train2["time2next"] = 0
              train2["passengers"] = []
              trains[tid] = train2
              tid = nextID(tid)
              cd2 = 5

      else:
        cd1 -= 1
        cd2 -= 1
    

      line["terminals"] = [(t1,cd1), (t2,cd2)]
      lines[ln] = line

  return [trains,tid]

def chuli(G, time):
  # 处理列车:
  global trains, passengers

  for tid in trains:
    t = trains[tid]
    if t["path"]: # 后面还有站点
      if t["time2next"] <= 0: # 该列车此刻到达站点
        curr_station = t["next_station"]
        del t["path"][0]
        if t["path"]:
          next_station = t["path"][0]
          time_cost = G.edges[(curr_station, next_station)]["time_cost"]
          t["time2next"] = time_cost
        else:
          next_station = None

        
        t["next_station"] = next_station

        # 处理乘客乘客
        # 列车上的乘客
        for pid in t["passengers"]:
          p = passengers[pid]
          if p["next_station"] == next_station: # 待在车上
            del p["path"][0]
            if p["path"]:
              p["next_station"] = p["path"][0]
            else:
              p["next_station"] = ''
            p["log"].append(f"上车：时间为{time}，列车为{tid}，上车站为{curr_station}，下一站为{next_station}")
          
          else: # 下车
            if p["path"]:
              t["passengers"].remove(pid)
              G.nodes[curr_station]["passengers"].append(pid)
              p["status"] = "候车"
              p["log"].append(f"下车：时间为{time}，列车为{tid}，车站为{curr_station}")
            else:
              t["passengers"].remove(pid)
              p["status"] = "已到达目的地"
              p["log"].append(f"到达目的地：时间为{time}，列车为{tid}，车站为{curr_station}")
        # 站点上的乘客
        for pid in G.nodes[curr_station]["passengers"]:
          p = passengers[pid]
          if p["next_station"] == next_station: # 上车
            G.nodes[curr_station]["passengers"].remove(pid)
            t["passengers"].append(pid)
            del p["path"][0]
            if p["path"]:
              p["next_station"] = p["path"][0]
            else:
              p["next_station"] = ''
            p["status"] = "乘车"
            p["log"].append(f"上车：时间为{time}，列车为{tid}，上车站为{curr_station}，下一站为{next_station}")
            passengers[pid] = p

      else:
        t["time2next"] -= 1

  return [G,passengers]

def commandPrompt(G,time):
  # User Input
  global trains, passengers
  global tid, pid

  while True:
    cmd = input("> ").split(' ')
    cmd_key = cmd[0]
    try:
      if cmd_key == "quit" or cmd_key == "q":
        return 0

      elif cmd==['']: # 时间向前一刻
        return 1

      elif cmd_key == "timeskip" or cmd_key == "ts":
        time_skip = int(cmd[1])
        return time_skip

      elif cmd_key == "new_passenger" or cmd_key == "np":
        source = cmd[1]
        target = cmd[2]
        
        if source not in G.nodes:
          print(f"Source {source} not found")
          continue
        if target not in G.nodes:
          print(f"Target {target} not found")
          continue

        # Create new passenger
        p = {}
        p["source"] = source
        p["target"] = target

        (p["path"], p["estimated_time"]) = shortest_path(G, p["source"], p["target"])
        p["start_time"] = time_int2str(time)
        p["end_time"] = ''
        del p["path"][0]
        p["next_station"] = p["path"][0]
        p["time2station"] = 0
        p["status"] = "候车" #0: 已到达，1：乘车，2：候车
        p["log"] = []
        passengers[pid] = p
        G.nodes[source]["passengers"].append(pid)
        print(f"New Passenger {pid}, source={source}, target={target}")
        pid = nextID(pid)

      elif cmd_key == "route" or cmd_key == "rt":
        source = cmd[1]
        target = cmd[2]
        (path, length) = shortest_path(G, source, target)
        print(f"路线：{path}")
        print(f"途径：{len(path)}站|预计时间：{length}分钟")

      elif cmd_key == "station" or cmd_key == "st":
        st_name = cmd[1]
        print(G.nodes[st_name])

      elif cmd_key == "passenger" or cmd_key == "p":
        PID = cmd[1]
        if PID == "list" or PID == "-l":
          print(passengers)
        else:
          print(passengers[PID])

      elif cmd_key == "train" or cmd_key == "t":
        TID = cmd[1]
        if TID == "list" or TID == "-l":
          print(trains)
        else:
          print(trains[TID])

      else:
        print(f"UNKOWN COMMAND \"{cmd_key}\"")
    except IndexError:
      print("ERROR: not enough input arguments")
    except KeyError:
      print(f"KeyError: {cmd[1]}")

  return True

def run(G, subwayinfo):
  createLines(subwayinfo)
  time = time_str2int("04:00") # 4AM

  global passengers, pid

  time_skip = 1
  while time_skip > 0:
    print(f"时间: {time_int2str(time)}")
    time_skip -= 1
    # 生成乘客
    newPassengers(G, time)

    # 生成列车
    newTrains(G, time)
    
    # 用户控制命令行
    if time_skip==0:
      time_skip = commandPrompt(G, time)

    #处理乘客与列车
    chuli(G, time)

    time += 1
  return

if __name__ == '__main__':
  print('~~~Start Simulation')
  city_id = sys.argv[1]
  subwayinfo = json.load(open(f'./data/{city_id}.json', 'r', encoding='utf-8'))
  G = createSubwayGraph(subwayinfo)
  
  run(G, subwayinfo)
  print('~~~Finish Simulation')