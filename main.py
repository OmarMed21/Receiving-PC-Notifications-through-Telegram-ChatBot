## Author: Omar Medhat Aly
## Company: Upwork
## Date Created: 06.06.2023

"""NOTE PART 1 SCRAPING THE DATA FROM NOTIFICATIONS OF WINDOWS AND SAVE THEM INTO A DICTIONARY"""

from winsdk.windows.ui.notifications.management import UserNotificationListener, UserNotificationListenerAccessStatus
from winsdk.windows.ui.notifications import NotificationKinds, KnownNotificationBindings
from winsdk.windows.foundation.metadata import ApiInformation
import asyncio
import time


if not ApiInformation.is_type_present("Windows.UI.Notifications.Management.UserNotificationListener"):
    print("UserNotificationListener is not supported on this device.")
    exit()

listener = UserNotificationListener.current

async def access_stat_func(lis) -> asyncio.coroutines:
    return await lis.request_access_async()
    
access_stat = asyncio.run(access_stat_func(listener))

async def notify(lis) -> asyncio.coroutines:
    return await lis.get_notifications_async(NotificationKinds.TOAST)

notifications = asyncio.run(notify(listener))

dic = {
    "App Name": [],
    "Notification Title": [],
    "Body Text": []
}

for i in notifications:
    text_sequence = i.notification.visual.get_binding(KnownNotificationBindings.toast_generic).get_text_elements()
    it = iter(text_sequence)
    dic['App Name'].append(i.app_info.display_info.display_name)
    dic['Notification Title'].append(it.current.text.encode('utf-8'))
    while True:
        next(it, None)
        if it.has_current:
            dic['Body Text'].append(it.current.text.encode('utf-8'))
        else:
            break 


"""NOTE PART 2 CREATING THE TELEGRAM BOT & SENDING THE INFORMATION"""

import requests

"""
    __________________
    | GET THE TOKEN  |
    ------------------

=> open /BotFather in telegram and start a chat
=> /newbot and create a bot with name you want
=> after those steps you will get HTTP API token (copy it) and save it to token variable
=> start chat with the chatbot you created and send anything
=> run the code above and get "id" and save it to variable chat_id

"""

## add the token here
token = '6316686314:AAHkWjBL57Ow_kqU8FFocHVXrd1HwsSAyx0'

## add the id here
chat_id = "1251062847"

"""NOTE: DON'T CHANGE THAT"""
while True:
    for name, notf, txt in zip(list(dic["App Name"]), dic['Notification Title'], dic["Body Text"]):
        if name == 'Google Chrome':
            message = f"App Name: {name}\nTitle: {notf}\nText: {txt}\n"
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(url).json()
        else: continue
    time.sleep(900) ## every 15 minutes

