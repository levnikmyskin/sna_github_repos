from get_data import save_user_and_enqueue_it, save_data, save_user_queue_contributors
import json
import traceback
from queue_luglio import queue


user_dict = json.load(open("luglio.json", 'r'))

try:
    save_user_queue_contributors(queue, user_dict)
    save_user_queue_contributors(queue, user_dict)
except:
    print("Abnormal interruption, saving data")
    print(traceback.format_exc())
finally:
    save_data(user_dict, "luglio2.json")
