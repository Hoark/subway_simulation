import configparser
import os

def read_config():
  config = configparser.ConfigParser()
  config.read('.\setup.cfg', encoding="utf-8")
  return config

if __name__ == '__main__':
  config = read_config()

  # Run data.py
  if config.getboolean('toRun', 'data.py'):
    execpath = config.get('DataParam', 'execpath')
    get_citylist = config.getboolean('DataParam', 'get_citylist')
    city_id = config.get('DataParam', 'city_id')
    os.system(f"python {execpath} {get_citylist} {city_id}")

  # Run simulation.py
  if config.getboolean('toRun', 'simulation.py'):
    execpath = config.get('SimulParam', 'execpath')
    city_id = config.get('SimulParam', 'city_id')
    source = config.get('SimulParam', 'source')
    target = config.get('SimulParam', 'target')
    os.system(f"python {execpath} {city_id} {source} {target}")
