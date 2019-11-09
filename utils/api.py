import requests
import time
import datetime
import hashlib

API_BASE_URL = 'http://127.0.0.1'            # Replace with your backend server's IP address
API_AUTH_USERNAME = 'YOUR_USERNAME_HERE'     # Replace with your registered username with proper permissions
API_AUTH_PASSWORD = 'YOUR_PASSWORD_HERE'     # Replace with your registered password with proper permissions

class API:
    def __init__(self):
        self.attendees_info_cache = {}
        self.session = requests.Session()
        self.login()
        self.get_attendees_info()
        print('[API] Initialization complete')

    def write_to_log(self, entry):
        with open('test.txt', 'a') as myfile:
            myfile.write('[' + str(datetime.datetime.now()) + '] ' + entry + '\n')

    def send_request(self, endpoint, data={}):
        retries = 0
        while retries < 5:
            try:
                req = self.session.post(API_BASE_URL + endpoint, json=data, timeout=10)
                if req.status_code == 401:
                    self.login()
                    continue
                return req.json()
            except Exception as e:
                retries += 1
            self.write_to_log('Request failure: ' + str(endpoint) + ' -> ' + str(data) + ' (' + str(e) + ')')
        return False

    def login(self):
        resp = self.send_request(
            '/api/v3/auth/login',
            data = {
                'username': API_AUTH_USERNAME,
                'password': API_AUTH_PASSWORD
            }
        )
        if not resp.get('is_authed'):
            raise Exception('Authentication failed: ' + str(resp))

    def get_attendees_info(self):
        resp = self.send_request('/api/v3/data/attendees_info')
        if len(resp.get('info', [])) == 0:
            raise Exception('Attendee info fetch failed: ' + str(resp))
        self.attendees_info_cache = resp['info']

    def return_existing_attendee_info(self, first_name, last_name):
        matching_attendees = []
        count = 0
        for x in range(0, 2):
            for attendee in self.attendees_info_cache:
                if first_name.lower() == attendee['first_name'].lower() and last_name.lower() == attendee['last_name'].lower():
                    matching_attendees.append(attendee)
            if len(matching_attendees) == 0:
                self.get_attendees_info()
            else:
                break
        return matching_attendees

    def create_attendee(self, first_name, last_name, designation):
        role = 'Student'
        if designation.split('-')[2] in ['LIT', 'T', 'L']:
            role = 'Helper'
        user_hash = hashlib.md5(first_name + '-' + last_name + '-' + designation).hexdigest()
        self.send_request(
            '/api/v3/checkin_client/create_attendee',
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'designation': designation,
                'role': role,
                'user_hash': user_hash
            }
        )
        self.get_attendees_info()

    def create_attendee_record(self, user_hash, marked_sunday_school):
        self.send_request(
            '/api/v3/checkin_client/submit_record',
            data = {
                'user_hash': user_hash,
                'checkin_ts': int(time.time()),
                'marked_sunday_school': marked_sunday_school
            }
        )
        self.get_attendees_info()
