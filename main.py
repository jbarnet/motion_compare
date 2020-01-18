from datetime import datetime, timezone, timedelta
from math import hypot

def partition_data_by_ids_and_sort(data_points):
  data_by_ids = {}
  for data_point in data_points:
    id = data_point['id']
    existing = data_by_ids.get(id, None)
    if existing:
      existing.append(data_point)
    else:
      data_by_ids[id] = [data_point]
  for id, data in data_by_ids.items():
    data_by_ids[id] = sorted(data, key=lambda x: x['timestamp'])
  return data_by_ids


def infer_matching_timeseries(desired_data, other_data):
  results = []
  for desired_item in desired_data:
    item_equal = None
    item_before = None
    item_after = None
    for other_item in other_data:
      if other_item['timestamp'] == desired_item['timestamp']:
        item_equal = other_item
        break
      elif other_item['timestamp'] < desired_item['timestamp']:
        item_before = other_item
      elif other_item['timestamp'] > desired_item['timestamp']:
        item_after = other_item
        break
    if item_equal:
      results.append(item_equal)  
    elif item_before and item_after:
      time_between = (item_after['timestamp'] - item_before['timestamp']).total_seconds()
      pre_offset = (desired_item['timestamp'] - item_before['timestamp']).total_seconds()
      post_offset = (item_after['timestamp'] - desired_item['timestamp']).total_seconds()
      x = (item_before['x'] * (pre_offset / time_between)) + (item_after['x'] * (post_offset / time_between))
      y = (item_before['y'] * (pre_offset / time_between)) + (item_after['y'] * (post_offset / time_between)) 
      results.append({
        'id': item_before['id'],
        'timestamp': desired_item['timestamp'],
        'x': x,
        'y': y
      })
  return results


def parse_overlap(desired_data, other_infered_data):
  results = []
  for other in other_infered_data:
    for desired in desired_data:
      if desired['timestamp'] == other['timestamp']:
        results.append(desired)
        continue
  return results


def compute_distances(desired_overlap_data, other_infered_data):
  results = []
  for other in other_infered_data:
    for desired in desired_overlap_data:
      if desired['timestamp'] == other['timestamp']:
        distance = hypot(desired['x'] - other['x'], desired['y'] - other['y'])
        results.append(distance)
        continue
  return results
    

def motion_compare(desired_id, data_points, min_overlap=3):
  data_by_ids = partition_data_by_ids_and_sort(data_points)
  desired_data = data_by_ids.get(desired_id, None)
  distances_by_id = []
  
  if desired_data:
    for id, data in data_by_ids.items():
      if id == desired_id:
        continue
      other_infered_data = infer_matching_timeseries(desired_data, data)
      desired_overlap_data = parse_overlap(desired_data, other_infered_data)
      distances = compute_distances(desired_overlap_data, other_infered_data)
      if len(distances) < min_overlap:
        continue
      distances_by_id.append({
        'id': id,
        'distances': distances,
        'average': sum(distances)/len(distances)
      })

  sorted_avg_distance = sorted(
    distances_by_id, 
    key=lambda x: x['average']
  )
  
  return sorted_avg_distance
    
start_time = datetime.utcnow().replace(tzinfo=timezone.utc)
def gen_test_data():
  data = []
  for id in range(2):
    for seconds in range(3):
      data.append({
        'id': str(id),
        'timestamp': start_time + timedelta(seconds=seconds),
        'x': seconds,
        'y': seconds    
      })
  return data



print(motion_compare('1', gen_test_data()))

 
 
  
  
    
    
  
  
      
