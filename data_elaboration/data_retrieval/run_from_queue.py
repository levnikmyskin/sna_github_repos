from get_data import save_user_and_enqueue_it, save_data, save_user_queue_contributors
import json
import traceback
import signal
from queue2135 import queue

def any_signal():
    save_data(user_dict, "depth4.json")

user_dict = json.load(open("depth3.json", 'r'))
for i in [s for s in dir(signal) if s.startswith("SIG")]:
    try:
        signum = getattr(signal, i)
        signal.signal(signum, any_signal)
    except:
        print("Skipping ", i)
try:
    save_user_queue_contributors(queue, user_dict)
    save_user_queue_contributors(queue, user_dict)
except:
   print("Abnormal interruption, saving data")
   print(traceback.format_exc())
finally:
    save_data(user_dict, "depth4.json")
