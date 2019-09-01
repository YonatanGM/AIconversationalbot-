from telethon import TelegramClient, events, utils
from telethon.tl.types import InputBotInlineResult
from datetime import datetime
import logging, argparse, os, subprocess
from googletrans import Translator
from mitsukuapi import mitsukuapi

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--TOKEN', required=True)
parser.add_argument('-i', '--api_id', type=int, required=True)
parser.add_argument('-q', '--api_hash', required=True)
args = parser.parse_args()

TOKEN = args.TOKEN
api_id = args.api_id
api_hash = args.api_hash


bot = TelegramClient('convbot', api_id, api_hash).start(bot_token=api_hash)

translator = Translator()


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    chat = await event.get_chat()
    await bot.send_message(chat,"ታዲያስ ፣ ሉሲ እባላለሁ። የመጀመሪያው ኢትዮጲያዊ ቻት ቦት ነኝ። ከ100 በላይ ቋንቋዎችን ስለምቸል በፈለጉት ቋንቋ ያዋሩኝ።\n\nHi, I am Lucy - the first universal language chat bot. Go ahead and talk to me in your desired language.")
    
    raise events.StopPropagation
    
@bot.on(events.NewMessage)
async def talk(event):
    chat = await event.get_chat()
    src = translator.detect(event.text)
    query = translator.translate(event.text, dest='en')
    print(query)
    reply = mitsukuapi(query.text)
    print(reply)
    print(src.lang)
    reply = translator.translate(reply, dest=src.lang)
    await bot.send_message(chat, reply.text)
      
        
bot.run_until_disconnected()

