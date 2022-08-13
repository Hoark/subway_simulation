# Subway
城市地铁数据爬取，地铁模拟系统构建

## Tutorial
1. 设置配置文件
2. 运行主控制代码，在命令行中输入```python main.py```
3. 使用命令列表中的命令与地铁模拟系统进行互动。
4. 退出，输入```quit```命令

## simulation.py命令列表
|命令|功能|示例|
|:---:|:---:|:---:|
|“回车”|时间向前一分钟|>|
|timeskip +amount|时间向前X分钟|> timeskip 60| 
|quit|退出|> quit|
|station +name|查询站点信息|> station 古城
|passenger +id|查询乘客信息|> passenger p0000000
|train +id|查询列车信息|> train t0000000
|new_passenger +source +target|创建乘客对象，起点为source，终点为target| >new_passenger 清华东路西口 五道口|

## 文件清单
|路径（默认）|功能说明|
|:-:|:-:|
|.\setup.cfg|配置文件：设置路径、参数等|
|.\main.py|主控制代码|
|.\code\baidu_data.py|从百度地图网站爬取所需要的数据|
|.\code\simulation.py|模拟地铁系统|
|.\code\subwaygraph.py|simulation.py辅助代码|
|.\code\utils.py|simulation.py辅助代码|
|.\data\citylist.json|城市列表，包括城市全名、城市简称、城市编号等的信息|
|.\data\xxx.json|编号为xxx的城市相关的地铁信息。地铁模拟系统是根据此信息而实现的|