from math import floor

def nextID(currID):
  currID = list(currID)
  for i in reversed(range(len(currID))):
    if (currID[i] >= '0' and currID[i]< '9') or (currID[i] >= 'a' and currID[i] < 'z'):
      currID[i] = chr(ord(currID[i]) + 1)
      break
    elif currID[i] == '9':
      currID[i] = 'a'
      break
    elif currID[i] == 'z':
      currID[i] = '0'
  return ''.join(currID)

def time_str2int(sTime):
  return int(sTime.split(':')[0])*60 + int(sTime.split(':')[1])

def time_int2str(iTime):
  return f"{floor(iTime/60):02d}:{iTime%60:02d}"

def status2str(status):
  # Currently not Used
  if status==0:
    return "已到达"
  elif status==1:
    return "乘车"
  elif status==2:
    return "候车"
  return ''

class Station(): # 站点（Graph中的Node）
  def __init__(self, name, pos=(0,0))->None:
    self.name = name # 站点名称
    self.pos = pos # 站点坐标位置
    self.passengers = [] # 在站点候车的乘客

  def __repr__(self) -> str:
    return "hello"

class Line(): # 路线（Graph中的Edge）
  def __init__(self, node1, node2, cost=0, colour="0x00000")->None:
    self.node1 = node1
    self.node2 = node2
    self.cost = cost
    self.colour = colour

  def __repr__(self)->str:
    pass

class Graph():
  def __init__(self):
    self.nodes = []
    self.edges = []
      

class Train():
  def __init__(self, train_id, path):
    self.id = train_id
    self.path = path
    self.passengers = []
    self.time2nextstation = 0
    self.log = []

class Passenger():
  def __init__(self, pass_id, source, target):
    self.id = pass_id
    self.source = source
    self.target = target
    self.path = []
    self.time2next_station = 0
    self.current_station = source
    self.next_station = target
    self.log = []
  def __repr__(self):
    return f"ID: {self.id}\nSource:{self.source}\nTarget:{self.target}"
