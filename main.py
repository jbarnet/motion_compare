from datetime import datetime

def infer_matching_timeseries(desired_data, other_data):
  

def motion_compare(desired_id, data_points):
  data_by_ids = {}
  for data_point in data_points:
    id = data_point['id']
    existing = data_by_ids.get(id, None)
    if existing:
      data_by_ids[id] = existing.append(data_point)
    else:
      data_by_ids[id] = [data_point]
  
  for id, data in data_by_ids.items():
    data_by_ids[id] = sorted(data, key=lambda x: x['timestamp'], reverse=True)
  
  desired_data = data_by_ids[desired_id]
  
  infered_data = {}
  for id, data in data_by_ids.items():
    if id == desired_id:
      continue
    infered_data[id] = infer_matching_timeseries(desired_data, data)
  
  distance_by_id = {}
  
    
    
  
  
      
