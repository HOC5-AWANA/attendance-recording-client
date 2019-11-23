import threading
import time
import traceback
from utils.api import API
from utils.prompt import create_attendee_record, clear_console

clear_console()
print('[MAIN] Initializing, please wait')

api = API()

def checkin_main():
    while True:
        try:
            checkin_data = create_attendee_record(api)
            if checkin_data:
                threading.Thread(target=threaded_create_record, args=[checkin_data]).start()
                print('Checked attendee in\n')
                time.sleep(5)
            else:
                print('Attendee not checked in, please retry')
                time.sleep(1.5)
        except Exception as e:
            api.write_to_log(str(traceback.format_exc()))
            print('[MAIN] Exception logged')
            time.sleep(1.5)

def threaded_create_record(info):
    user_hash, marked_sunday_school = info
    api.create_attendee_record(user_hash, marked_sunday_school)
    print('Color recommendation: ' + api.get_color_recommendation(user_hash) + '\n')

clear_console()
print('[MAIN] Initialization complete')
time.sleep(3)

checkin_main()
