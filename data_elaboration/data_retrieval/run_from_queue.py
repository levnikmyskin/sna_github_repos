from get_data import save_user_and_enqueue_it, save_data, save_user_queue_contributors
import json
import traceback
from queue2135 import queue

user_dict = json.load(open("depth3.json", 'r'))
try:
    save_user_queue_contributors(queue, user_dict)
    save_user_queue_contributors(queue, user_dict)
except:
   print(traceback.format_exc())
finally:
    save_data(user_dict, "depth4.json")
