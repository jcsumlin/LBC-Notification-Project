import requests
import json


class Notify():
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://www.notifymydevice.com/push"

    def notify(self, title, message):
        self.notification_title = title
        self.notification_message = message
        return self.send(self.notification_title, self.notification_message)

    def send(self, title, message):
        self.data = {"ApiKey": self.api_key, "PushTitle": title,"PushText": message}
        self.headers = {'Content-Type': 'application/json'}
        r = requests.post(self.url, data=json.dumps(self.data), headers=self.headers)
        if r.status_code == 200:
            return('Notification sent!')
        else:
            return('Error while sending notificaton!')
