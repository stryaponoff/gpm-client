import re
import os
from gmusicapi import Mobileclient
from dotenv import load_dotenv


class GMusicApp:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.cred_filename = os.path.join(self.base_dir, 'credentials.json')
        self.api = Mobileclient()

    @staticmethod
    def get_device_id():
        dev_id = os.getenv('DEVICE_ID')

        if not dev_id:
            raise Exception('Please fill the DEVICE_ID field in .env file')
        elif not re.match('^[a-f0-9]*$', dev_id):
            raise Exception('DEVICE_ID is incorrect')

        return dev_id

    def auth(self):
        try:
            device_id = self.get_device_id()
        except Exception as e:
            raise e

        if not os.path.exists(self.cred_filename):
            self.api.perform_oauth(self.cred_filename, False)

        return self.api.oauth_login(device_id, self.cred_filename)

    def run(self):
        playlists = self.api.get_all_playlists()
        print(playlists)


if __name__ == '__main__':
    load_dotenv()

    try:
        app = GMusicApp()
        if app.auth():
            app.run()
    except Exception as e:
        print(getattr(e, 'message', e))
