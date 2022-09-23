from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import pytz as pytz

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
beijing_now = utc_now.astimezone(SHA_TZ)
niw = beijing_now.strftime("%Y/%m/%d %H:%M:%S")

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

# def get_now_time():
#     a = datetime.now()
#     b = a.strftime("%Y/%m/%d %H:%M:%S")
#     return b

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), weather['wind'], weather['humidity']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days+1

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,wind,humidity = get_weather()
# now = get_now_time()
data = {

        "weather":{"value":wea}, #天气
        "temperature":{"value":temperature},
        "now": {"value": now},
        "wind":{"value":wind},
        "city":{"value":"杨陵示范区","color":"#1c4587"},
        "humidity":{"value":humidity},
        "love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday(),"color":"#980000"},
        "words":{"value":get_words(), "color":get_random_color()}}


res = wm.send_template(user_id, template_id, data)
