import configparser
from notify import Notify
import LocalBitcoin
import os
import time

config = configparser.ConfigParser()
config.read('auth.ini')
api_key = str(config.get('auth', 'notify_my_android'))
# hmac_auth_key = os.environ['hmac_auth_key']
hmac_auth_key = str(config.get('auth', 'hmac_auth_key'))  # REQUIRED
# hmac_auth_secret = os.environ['hmac_auth_secret']
hmac_auth_secret = str(config.get('auth', 'hmac_auth_secret'))  # REQUIRED

n = Notify(api_key)
lc = LocalBitcoin.LocalBitcoin(hmac_auth_key, hmac_auth_secret, False)

if not os.path.isfile("notifications_sent.txt"):
    notifications_sent = []
else:
    with open("notifications_sent.txt", "r") as f:
        notifications_sent = f.read()
        notifications_sent = notifications_sent.split("\n")
        notifications_sent = list(filter(None, notifications_sent))

def update_files(notifications_sent):
    with open("notifications_sent.txt", "w") as f:
        for x in notifications_sent:
            f.write(x + "\n")

def main():
    messages = lc.getRecentMessages()
    notifications = lc.getNotifications()
    for message in messages['message_list']:
        message_info = str(message['created_at']) + ' ' + str(message['contact_id']) + ' ' + str(message['sender']['name'])
        message_author = str(message['sender']['username'])
        if message_info not in notifications_sent:
            if message_author != "J_C":
                print(str(message['sender']['username']))
                if str(message['msg'].encode('utf-8')) == '':
                    message_contents = 'Message Field Is Empty'
                    if 'attachment_url' in message:
                        message_contents = message_contents + '\n' + message['attachment_url']
                else:
                    if 'attachment_url' in message:
                        message_contents = str(message['msg'].encode('utf-8')) + '\n' + message['attachment_url']
                    else:
                        message_contents = str(message['msg'].encode('utf-8'))
                n.notify(str(message['sender']['name']) + ' - ' + str(message['contact_id']), message_contents)
                print("------\nMessage Sent\n")
            elif message_author == "J_C":
                print("------\nMessage From Me")
            notifications_sent.append(message_info)
            update_files(notifications_sent)
    print("------\nReached End of List")

try:
    while True:
        main()
        print("------\nIdling for 20s\n")
        time.sleep(20)
except Exception:
    pass