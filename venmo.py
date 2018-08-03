import requests
import json
import networkx as nx
import time
class Person:
  def __init__(self, first_name, last_name, internal_id):
    self.first_name = first_name
    self.last_name = last_name
    self.internal_id = internal_id
G = nx.DiGraph()
seen_people = set()
num_req = 0
page = "https://venmo.com/api/v5/public"
try:
  while num_req < 250:
    response = requests.get(page)
    if response.status_code == 200:
      num_req += 1
      info = json.loads(response.content)
      #print(info['paging']['previous'])
      page = info['paging']['previous']
      for d in info['data']:
        sender = d['actor']
        receiver = d['transactions']
        s = Person(sender['firstname'], sender['lastname'], sender['id'])
        for m in receiver:
          rec = m['target']
          if isinstance(rec, dict):
            r = Person(rec['firstname'], rec['lastname'], rec['id'])
          else:
            r = Person('invalid', 'invalid', 'invalid')
        if d['type'] == 'payment':
          if s.internal_id not in seen_people:
            seen_people.add(s.internal_id)
            G.add_node(s.internal_id, name=s.first_name + ' ' + s.last_name)
          if r.internal_id not in seen_people:
            seen_people.add(r.internal_id)
            G.add_node(r.internal_id, name=r.first_name + ' ' + r.last_name)
          G.add_edge(s.internal_id, r.internal_id, message=d['message'], date=d['created_time'])
        else:
          if s.internal_id not in seen_people:
            seen_people.add(s.internal_id)
            G.add_node(s.internal_id, name=s.first_name + ' ' + s.last_name)
          if r.internal_id not in seen_people:
            seen_people.add(r.internal_id)
            G.add_node(r.internal_id, name=r.first_name + ' ' + r.last_name)
          G.add_edge(r.internal_id, s.internal_id, message=d['message'], date=d['created_time'])
    else:
      print(response.status_code)
      print('number of requests completed: %d' % num_req)
      print('current page: ' + page)
      time.sleep(15)
  nx.write_gexf(G, "new.gexf")

except KeyboardInterrupt:
  print(num_req)
  nx.write_gexf(G, "new.gexf")
  

