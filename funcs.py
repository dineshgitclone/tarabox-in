# funcs
import time
import re,os
import requests as rq
from database import *
from pyrogram import Client
from transcripts import *

# from unshortenit import UnshortenIt
sudo_users = [1953040213, 5144980226, 874964742,839221827, 5294965763,5317652430,5141357700]
TOKEN = os.environ.get("BOT_TOKEN", "5803666114:AAEBnB7upQXTv_5KlPq7vzT-jJ2q3nzn52k")
API_HASH = os.environ.get("API_HASH", "cceefd3382b44d4d85be2d83201102b7") 
API_ID = os.environ.get("API_ID", "10956858")


bot = Client("Url-Short-Bot", api_id=API_ID,
             api_hash=API_HASH, bot_token=TOKEN, workers=10)


# URL Shortner
SHORT_API = '233f81db4b3afb2cfc1be7e0cad4d6b066b7cbb5'
API_PTN = r'[a-z0-9]{35,43}'

REAL_URL = 'https://ez4short.com/api?'
url_ptrn = r'https?://[^\s]+'


def short_urls(url_list, URL_API=SHORT_API,DOMAIN = 'tarabox.in'):
    cnvt_urls = []
    
    for link in url_list:

        # if ('bit' in link ):
        #		      unshortener = UnshortenIt()
        #		      link = unshortener.unshorten(link)

        param = {'api': URL_API, 'url': link}
        try:
            res = (rq.get(REAL_URL, params=param))
        # res=(rq.get(r_url.format(r_token,link)))
            data = dict(res.json())
            link = data['shortenedUrl']
            # link = link.replace('tarabox.in',DOMAIN)
            cnvt_urls.append(link)

        except ConnectionResetError:
            cnvt_urls.append("Failed To Convert")
    
            
        except:
            cnvt_urls.append(link)

    return cnvt_urls


def filter_tele_urls(urls):
    f_urls = []
    for link in urls:
        if 't.me' in link:
            pass
        else:
            f_urls.append(link)
    return f_urls


def convert_post(msg_text, Api,replace_item,Domain):

    # msg_text=msg_text.text
    list_string = msg_text.splitlines()
    msg_text = ' \n'.join(list_string)
    new_msg_text = list(map(str, msg_text.split(" ")))
    new_join_str = "".join(new_msg_text)

    urls = re.findall(url_ptrn, new_join_str)
    urls = filter_tele_urls(urls)

    nml_len = len(new_msg_text)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_msg_text[i]):
                url_index.append(count)
        count += 1
    new_urls = short_urls(urls,URL_API=Api,DOMAIN = Domain)
    url_index = list(dict.fromkeys(url_index))
    i = 0

    for j in url_index:
        new_msg_text[j] = new_msg_text[j].replace(urls[i], new_urls[i])
        i += 1
    caption = " ".join(new_msg_text)
    caption = replace_telegram_urls(caption,replace_item)
    return caption


def replace_telegram_urls(input_string,replce_value):
    # Regular expression to match a Telegram URL
    telegram_regex = r"https://t.me/\S+"

    # Split the input string into chunks of up to 1000 characters each
    chunk_size = 4000
    chunks = [input_string[i:i+chunk_size] for i in range(0, len(input_string), chunk_size)]

    # Replace Telegram URLs with "http://google.com" in each chunk
    updated_chunks = []
    for chunk in chunks:
        updated_chunk = re.sub(telegram_regex, replce_value, chunk)
        updated_chunks.append(updated_chunk)

    # Join the updated chunks back into a single string
    updated_string1 = "".join(updated_chunks)
    updated_string = replace_telegram_usernames(updated_string1,replce_value)

    return updated_string

def replace_telegram_usernames(input_string,replce_value):
    # Regular expression to match Telegram usernames
    username_regex = r"@\w+"

    # Replace usernames with "http://google.com"
    updated_string = re.sub(username_regex, replce_value, input_string)

    return updated_string




# progress bar Funciton
async def progress_msg(m):
    msg = await m.reply_text(progress_txt)
    return msg
