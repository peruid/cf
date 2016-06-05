#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import telebot
import logging
from random import randrange
import json
import requests
import os
import sys

# logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename='telegram_bot.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
botlog = logging.getLogger('telegram')


tb = telebot.TeleBot(config.bot['token'])

def jira_filter(f):
    r = requests.get(config.jira['api_url'] + '/filter/' + str(f), auth=('zabbix', 'newpassword'), verify=False)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return json.loads('')

def jira_srch(url):
    r = requests.get(url, auth=('zabbix', 'newpassword'), verify=False)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return json.loads('')

def check_admin(message):
    #                          Dambaev                             Udovenko                             Efremov
    if message.from_user.id == 77889509 or message.from_user.id == 127280273 or message.from_user.id == 92181860:
        return True
    else:
        return False

@tb.message_handler(commands=['start', 'id'])
def handle_start_id(message):
    text = u"Laat me alleen alstublieft\n"
    text += "Your id: "+str(message.from_user.id)
    if message.chat.id != message.from_user.id:
      text += "\nGroup ID: "+str(message.chat.id) 
    tb.send_message(message.chat.id, text)


@tb.message_handler(commands=['help'])
def echo_help(message):
    text = '''
User commands are:
/id
        '''
    if check_admin(message):
        text += '''
Staff commands are:
/jt - List Tasks (Jira filter: 15423)
/ji - List Incidents (Jira filter: 15417)
/restart - Restarts the bot process (about a minute)
        '''
    tb.send_message(message.from_user.id, text)

def report_filter(filter, message):
    tb.send_chat_action(message.chat.id, 'typing')
    flt = jira_filter(filter)
    issues = jira_srch(flt['searchUrl'])
    if issues['total'] >= 1:
        header = flt['name'] + ": " + str(issues['total']) + "\n"
        text = header
        for i in issues['issues']:
            if i['fields']['assignee'] == None:
                i['fields']['assignee'] = { 'name':'-' }
            text += "- " + i['fields']['summary'] + " (" + i['key'] + ") " + "[" + i['fields']['assignee']['name'] + "]\n"
            if len(text) > 1850:
                tb.send_message(message.chat.id, text)
                text = header
        if len(text) > 100:
            tb.send_message(message.chat.id, text)
    else:
        tb.send_photo(message.chat.id, open('ne_pizdi.jpg', 'rb'))

@tb.message_handler(commands=['jt','ji'])
def jira_report(message):
    if message.text == '/jt':
        f_id = 15423 # Duty tasks in DEVOPSDUTY
    elif message.text == '/ji':
        f_id = 15417 # incidents
    if f_id != None:
        if check_admin(message):
            pass
        else:
            message.chat.id = message.from_user.id
        report_filter(f_id, message)

@tb.message_handler(commands=['restart'])
def restart_cmd(message):
    if check_admin(message):
        tb.send_message(message.chat.id, 'Restarting ... I\'ll be back, if cron setup properly')
        sys.exit()

@tb.message_handler(content_types=['sticker'])
def sticker_react(message):
    if check_admin(message):
        tb.send_message(message.from_user.id, str(dump(config.bot['sticker'])))

@tb.message_handler(func=lambda message: True, content_types=['text'])
def log_msg(message):
    botlog.info(message.text)

def listener(messages):
    for m in messages:
        botlog.info(str(m))

tb.set_update_listener(listener)
tb.send_message(77889509, 'Started...')
tb.polling(none_stop=True)
