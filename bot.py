
# telebot is needed
# Pillow is needed
# numpy is needed
# requests is needed
#  opencv is needed http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
# tesseract is needed sudo apt-get install tesseract-ocr
import telebot
from PIL import Image, ImageFilter
import numpy as np
import requests
import os
from dss import *
import logging


def printutf8(s, ofile=sys.stdout.buffer):
    pass

secret = ""
with open("./secret.txt", "r") as f:
    secret = f.readline().rstrip('\n')

bot = telebot.TeleBot(secret)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I'm a @dsspiebot!\nSend me a phrase and some different conclusion of that phrase and I tell you which is the online popularity.\nExample:\n/pie\nI like\nfoods\ncats", parse_mode="HTML")

@bot.message_handler(commands=['pie'])
def echo_all(message):
    chat_id = message.chat.id
    mex = message.text.replace("/pie "," ")
    logging.info('Request: '+mex.replace("\n"," / "))
    try:
        out = "Please send the statment"
        msg = bot.send_message(chat_id, out, parse_mode="HTML")
        bot.register_next_step_handler(msg,process_head_step)
    except ValueError as E:
        logging.error('Errore: '+mex+" "+str(E))
        bot.reply_to(message, mex+": errore interno.")

def process_head_step(message):
    try:
        chat_id = message.chat.id
        head = message.text
        out = "Send me the first option for (<i>"+str(head)+"</i>)"
        msg = bot.send_message(chat_id, out, parse_mode="HTML")
        bot.register_next_step_handler(msg,process_option_step,head,[])
    except Exception as e:
        bot.reply_to(message, 'You are wrong')


def process_option_step(message, head, options):
    try:
        chat_id = message.chat.id
        option = message.text
        if not option == "done" and not option == "/done":
            options.append(option)
            out = "Send me the next option for (<i>"+str(head)+"</i>)\nSend /done when you have done."
            msg = bot.send_message(chat_id, out, parse_mode="HTML")
            bot.register_next_step_handler(msg,process_option_step,head,options)
        else:
            bot.send_chat_action(chat_id, 'upload_photo')
            def load():
                bot.send_chat_action(chat_id, 'upload_photo')
            pie = searchComplete(head,options, load)
            if(pie!=None):
                bot.send_photo(chat_id, pie, caption = " @dsspiebot")
            else:
                bot.reply_to(message, "Request is not properly formatted.\nNeed /help?")
    except Exception as e:
        bot.reply_to(message, 'You are wrong'+str(e))


@bot.message_handler(commands=['chatid'])
def echo_all(message):
    cid = message.chat.id
    bot.reply_to(message, " chat id: "+str(cid))

@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    pass

while(True):
    try:
        #bot.polling(none_stop = True, interval = 3)
        bot.infinity_polling(True)
    except Exception as e:
        print("[%s] error on bot polling" % (datetime.datetime.now()))
        time.sleep(30)
