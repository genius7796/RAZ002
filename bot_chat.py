# see 'main.py'
import os
from urllib import response

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium import webdriver
from pynput import keyboard
from slugify import slugify
from fancy import Fancy
import pyautogui as gui
from animu import client as acl
from random import randint
import http.client
import wikipedia
import asyncio
import requests
import socket
import emoji
import random
import json
import gc
import os
from selenium.webdriver.firefox.options import Options
from apiclient.discovery import build
from youtubesearchpython import VideosSearch

options = Options()
options.headless = False

waifu = acl.Client("eae6c4c7e1a3fffe31e383371dd477d82649ac579117")
profile = FirefoxProfile("/home/raz0229/.mozilla/firefox/58m1hr3k.dev-edition-default")

blocked_list = ["mom", "dad", "mother", "father", "mommy", "moma", "mama", "sister", "sissy",  "lu", "phudi", "phodi", "chut", "bund", "bond", "fuck", "gashti", "pencho"]
blocked_names = ["talh", "batol", "raz", "abdulh", "wahb", "janua", "jinua", "raj", "zafr", "janu", "nor", "tlha", "btol", "mustaf", "ali", "chris", "an"]

# Configuration
PATH = "/home/raz0229/Downloads/geckodriver"  # path to your downloaded webdriver
driver = webdriver.Firefox(profile, executable_path=PATH, options=options)
driver.get('https://instagram.com/direct/inbox')
print(driver.title)  # prints title of the webpage

conn = http.client.HTTPSConnection("aeona3.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "85632300dbmsha01f5765f1a7303p18df83jsn83e04aa1780a",
    'X-RapidAPI-Host': "aeona3.p.rapidapi.com"
    }

connTranslate = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")
headersTranslate = {
    'content-type': "application/x-www-form-urlencoded",
    'Accept-Encoding': "application/gzip",
    'X-RapidAPI-Host': "google-translate1.p.rapidapi.com",
    'X-RapidAPI-Key': "85632300dbmsha01f5765f1a7303p18df83jsn83e04aa1780a"
    }


def deemojify(text):
    return emoji.get_emoji_regexp().sub(r'', text)


def urlify(text, command, target):
    slug = slugify(text.lower().replace(command, '').strip(), separator='%20')
    return f"q={deemojify(slug)}&target={target}"


def load_requests(source_url, sink_path):
    import requests
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(sink_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def filter_word(word):
    res = [ele for ele in blocked_list if (ele in word)]
    if res:
        return []
    word = ''.join(sorted(set(word), key=word.index))
    res = [ele for ele in blocked_names if (ele in word)]
    return res


def search_youtube_url(videoQuery):
    videosSearch = VideosSearch(f'{videoQuery}', limit = 5)
    if len(videosSearch.result()['result']) >= 1:
       num = random.randrange(0, 5)
       return videosSearch.result()['result'][num]['link']
    return "🤖🦇 No matching video found"


def search_video_url(videoQuery):
    ftr = [3600,60,1]
    url = ''

    videosSearch = VideosSearch(f'{videoQuery} 30 seconds', limit = 5)
    videos = videosSearch.result()['result']
    for i in range(len(videos)):
        duration = videos[i]['duration']
        timestr = duration
        if duration is not None:
            timestr = duration if len(duration.split(':')) >= 3 else f"00:{duration}"
        checkDuration = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]) if timestr is not None else "None"
        if checkDuration <= 60: 
            url = videos[i]['link']
            break
    return url

class Bot:
    def __init__(self, contact):
        self.contact = contact
        elem = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, f'//*[text() = "{self.contact}" ]')))
        elem.click()
        self.incoming = WebDriverWait(driver, 120).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR ,'._aacl._aaco._aacu._aacx._aad6._aade')))
        self.received_msgs = len(self.incoming)
        self.running = True
        self.pressed_ctrl = False

    def make_call(self, request):
        
        conn.request("GET", f"/?text={slugify(request)}&userId=12312312312", headers=headers)
        
        try:
            res = conn.getresponse()
            data = res.read()
            response = data.decode("utf-8")
        except socket.timeout:
            return "ERR: Slow Internet connect on host"
        except http.client.HTTPException:
            self.make_call(request)
        else:  # no error occurred
            return response.replace('Aeona', 'RAZBot').replace('Oakland, California', 'RazRiG')  # replace name and location in response

    def new_msg_received(self):
        incoming = driver.find_elements_by_css_selector('._aacl._aaco._aacu._aacx._aad6._aade')
        if len(incoming) != self.received_msgs:
            return True
        else:
            return False

    def send_message(self, text):
        input_box = driver.find_element_by_css_selector('textarea')
        input_box.click()
        input_box.send_keys(text, Keys.RETURN)
        incoming = driver.find_elements_by_css_selector('._aacl._aaco._aacu._aacx._aad6._aade')
        self.received_msgs = len(incoming)

    def send_copied_image(self):
        input_box = driver.find_element_by_css_selector('textarea')
        input_box.click()
        input_box.send_keys(Keys.LEFT_CONTROL, "v")
        send_button = driver.find_element_by_css_selector("._acan._acap._acaq._acas._acav")
        send_button.click()
        incoming = driver.find_elements_by_css_selector('._aacl._aaco._aacu._aacx._aad6._aade')
        self.received_msgs = len(incoming)

    def on_press(self, key):
        print(key, 'Key pressed')
        if key == keyboard.Key.ctrl_r:  # If 'Left Ctrl' is the key pressed
            try:
                self.pressed_ctrl = True
            except Exception as e:
                print(f'{self.contact}: No such contact')
                print(e)
                pass

    def init_bot(self):
        while self.running:
            if self.new_msg_received():

                    try:
                        self.incoming = driver.find_elements_by_css_selector('._aacl._aaco._aacu._aacx._aad6._aade')
                        self.received_msgs = len(self.incoming)
                        last_msg = self.incoming[self.received_msgs - 1].text
                        print(last_msg)
                        if not last_msg.startswith('💀🦇'):
                            print(last_msg)
                            self.send_message('💀🦇 ' + self.make_call(deemojify(last_msg.strip())))
                    except Exception:
                        last_msg = 'Something exception'

                    # BOT response
 #                   if last_msg.lower().startswith(""):
     #                   self.send_message('Thinking... 💀🦇')

    #                    if deemojify(last_msg.lower().strip()) == "bot_ask":
   #                         self.send_message("🤖🦇 Chat with me using bot_ask command. Example: bot_ask who are you")
  #                      else:
 #                           self.send_message(self.make_call(deemojify(last_msg.replace("bot_ask", '').strip())))
#
#                    else:
#                        print("No command")
            if self.pressed_ctrl:
                break
        self.contact = gui.prompt('Enter contact\'s name', 'WhatsApp Chat bot')
        print(self.contact, type(self.contact))
        driver.find_element_by_xpath(f'//*[text() = "{self.contact}" ]').click()
        self.pressed_ctrl = False
        self.init_bot()

    # In case you have to stop the program for some reason
    def stop_bot(self):
        self.running = False
        print('Bot stopped')
        gc.collect()
