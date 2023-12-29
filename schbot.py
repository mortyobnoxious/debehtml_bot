import os
import telebot
import requests
from datetime import datetime, time, timedelta
import re
import os.path
import schedule
import time as t
from bs4 import BeautifulSoup

BOT_TOKEN = ''
# How to get Channel ID https://gist.github.com/mraaroncruz/e76d19f7d61d59419002db54030ebe35
CHANNEL_ID = ''

bot = telebot.TeleBot(BOT_TOKEN)

print("Starting...")

def htmlEntryBase(title, divs):
    return f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%2381c14b' viewBox='0 0 18 18'%3E%3Cpath d='M6.71981 17.3999C3.55072 17.3999 1 14.8492 1 11.6801C1 8.58831 6.71981 1.3999 6.71981 1.3999C6.71981 1.3999 12.4396 8.58831 12.4396 11.6801C12.4396 14.8492 9.88889 17.3999 6.71981 17.3999ZM6.71981 17.3999C6.7971 17.3999 6.7971 17.3999 6.71981 17.3999Z' stroke-width='1.3'%3E%3C/path%3E%3C/svg%3E" type="image/svg+xml"/>
<style type="text/css">
html {{background: #1b2836;color: #8798A5;font-family: Calibri;}}
body {{width: 600px;max-width: calc(100% - 20px);margin: 10px auto 0 auto;counter-reset: debe;}}
.gen {{display: flex;flex-direction: column;background: #15212d;margin-bottom: 15px;box-shadow: 2px 3px 3px rgba(0,0,0,0.52);}}
.entry {{padding: 0 10px;line-height: 1.3;letter-spacing: .2;word-break: break-word;}}
.footer {{display: flex;justify-content: space-between;padding: 5px 5px;border-top: 1px solid #1b2836;margin-top: 5px;gap: 20px;}}
.footer a {{color: #5C6570;font-size: 12px;}}
.footer a:last-child {{border-left: 2px solid #1b2836;padding-left: 5px;}}
.footer span[data-fav] {{display: flex;align-items: center;justify-content: center;gap: 3px;font-size: 12px;color: #bdbdbd;}}
.footer span[data-fav="0"] {{opacity: 0;}}
.footer > span:not([data-fav]) {{display: flex;gap: 5px;}}
.footer svg {{width: 12px;height: 12px;fill: #1b2836;stroke: #bdbdbd;}}
h1 {{font-size: 1.1rem;background: #10171f;padding: 3px 8px;margin: 0 0 10px 0;}}
h1 a {{color: #A9894F;text-decoration: none;}}
h1.debe {{display: flex;align-items: center;gap: 5px;position: sticky;top: 0;}}
h1.debe::before {{content: counter(debe);counter-increment: debe;border-right: 1px solid #1b2836;padding-right: 5px;}}
a {{color: #81C14B;text-decoration: none;}}
a:hover {{color: #fff !important;transition: all .3s !important;}}
.url {{display: inline-flex;align-items: center;gap: 3px;}}
.url::after {{content: "🔗";font-size: 10px;}}
.ab a::after {{content: "("attr(data-query)")";font-size: 10px;}}
.read-more {{display: block;margin: 10px 0 0 0;font-style: italic;}}
.read-more span {{margin-right: 8px;background-color: #323f4b;border-radius: 10%;padding: 0 3px;color: #8798A5;}}
.read-more + .more-text {{display: none;}}
</style>
</head>
<body>
{divs}
<script>
const ENTRY = document.querySelectorAll('.entry');
const H1 = document.querySelectorAll('.gen > h1');
function truncateNode(e,n=20){{var t=e.innerHTML.match(/<[^>]+>|[^<>]+/g),i=t.slice(0,n).join(" "),n=t.slice(n,e.length).join(" ");e.innerHTML.length>i.length&&n.length>i.length&&(i=`${{i}} <a href="javascript:void(0);" onclick="readMore(this)" class="read-more"><span>...</span>devamını okuyayım</a><span class='more-text'>${{n}}</span>`,e.innerHTML=i)}}
function readMore(e){{e.nextSibling.replaceWith(...e.nextSibling.childNodes),e.remove()}}
1<ENTRY.length&&H1.forEach(e=>{{e.classList.add("debe")}}),
ENTRY.forEach(e=>{{truncateNode(e)}});
</script>
</body>
</html>
"""


def htmlEntryTemp(title, entry, id, author, date, fav=0):
    entry = re.sub(r'href="\/', 'href="https://eksisozluk.com/', entry)
    entry = re.sub(r'class="b"', 'class="b" target="_blank"', entry)
    return f"""
<div class="gen">
<h1><a href="https://eksisozluk.com/?q={title}" target="_blank">{title}</a></h1>
<div class="entry">{entry}</div>
<div class="footer">
<span data-fav="{fav}"><svg class="eksico"><use xlink:href="#eksico-drop"><symbol id="eksico-drop" viewBox="0 0 14 19">
    <path d="M6.71981 17.3999C3.55072 17.3999 1 14.8492 1 11.6801C1 8.58831 6.71981 1.3999 6.71981 1.3999C6.71981 1.3999 12.4396 8.58831 12.4396 11.6801C12.4396 14.8492 9.88889 17.3999 6.71981 17.3999ZM6.71981 17.3999C6.7971 17.3999 6.7971 17.3999 6.71981 17.3999Z" stroke-width="1.3"></path>
  </symbol></use></svg>{fav}</span>
<span>
<a href="https://eksisozluk.com/entry/{id}" target="_blank">{date}</a>
<a href="https://eksisozluk.com/biri/{author}" target="_blank">@{author}</a>
</span>
</div>
</div>
"""
def isBetween(begin_time, end_time, check_time=None):
    check_time = check_time or (datetime.utcnow() + timedelta(hours=3)).time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time

aylar = ["", "Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
gunler = ["Paz", "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt"]

def getDocTitle():
    x = datetime.utcnow() + timedelta(hours=3)
    if isBetween(time(0,0), time(7,35)):
        x = x - timedelta(days=1)
    ay = x.strftime("%m")
    gun = x.strftime("%w")
    tarih = x.strftime("%d")
    yil = x.strftime("%Y")
    docTitle = f"debe {str(tarih)} {str(aylar[int(ay)])} {str(yil)} {str(gunler[int(gun)])}.html"
    return docTitle

DEBE_LIST = []
def getDebeList():
    global DEBE_LIST
    URL = "https://eksisozluk.com/m/debe"
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    ul = soup.select('.topic-list.partial.mobile > li > a')
    for a in ul:
        DEBE_LIST.append(a["href"].replace('/entry/',''))

    def getDebe():
        global DEBE_LIST
        divs = ''
        for id in DEBE_LIST:
            URL = "https://eksisozluk.com/entry/" + id
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            li = soup.select_one('#entry-item')

            idm = id
            title = soup.select_one('#title').text.strip()
            entry = str(li.select_one('.content').decode_contents()).strip()
            author = li.select_one('.entry-author').text.strip()
            fav = li["data-favorite-count"].strip()
            date = li.select_one('.entry-date').text.strip()
            div = htmlEntryTemp(title, entry, idm, author, date, fav)
            divs += div

        html = htmlEntryBase(getDocTitle().replace('.html', ''), divs)
        with open(r'/tmp/'+getDocTitle(), "w", encoding="utf-8") as write_file:
            print(f"{html}", file=write_file)
        DEBE_LIST = []
    getDebe()

def getDebeSozlock():
    URL = "https://sozlock.com"
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    ul = soup.select('ul.entrylist > li')
    divs = ''
    for li in ul:
        idm = li.select_one('a[title="orjinalini gör"]')['href'].split('entry/')[1]
        tiraw = li.select_one('h3').text.strip()
        title = re.sub("^\d+\. ", "", str(tiraw))
        entry = str(li.select_one('.entrytxt').decode_contents()).strip()
        author = li.select_one('a.yazar').text.strip()
        fav = li.select_one('.votecurrent').text.strip().replace('-','0')
        date = li.select_one('.entrytime').text.strip()
        div = htmlEntryTemp(title, entry, idm, author, date, fav)
        divs += div

    html = htmlEntryBase(getDocTitle().replace('.html', ' [sozlock]'), divs)
    with open(r'/tmp/'+getDocTitle().replace('.html', ' [sozlock].html'), "w", encoding="utf-8") as write_file:
        print(f"{html}", file=write_file)

def logFiles():
    tmp_dir = '/tmp/'
    for file_name in os.listdir(tmp_dir):
        file_path = os.path.join(tmp_dir, file_name)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            print(f"File: {file_name}, Size: {file_size} bytes")

logFiles()

def job():
    if os.path.isfile(r'/tmp/'+getDocTitle()):
        doc = open(r'/tmp/'+getDocTitle(), 'rb')
        bot.send_document(CHANNEL_ID, doc)
    else:
        getDebeList()
        doc = open(r'/tmp/'+getDocTitle(), 'rb')
        bot.send_document(CHANNEL_ID, doc)

def jobsec():
    if os.path.isfile(r'/tmp/'+getDocTitle().replace('.html', ' [sozlock].html')):
        doc = open(r'/tmp/'+getDocTitle().replace('.html', ' [sozlock].html'), 'rb')
        bot.send_document(CHANNEL_ID, doc)
    else:
        getDebeSozlock()
        doc = open(r'/tmp/'+getDocTitle().replace('.html', ' [sozlock].html'), 'rb')
        bot.send_document(CHANNEL_ID, doc)

schedule.every().day.at("04:45").do(job)
schedule.every().day.at("04:50").do(jobsec)

while True:
    schedule.run_pending()
    t.sleep(60) #1 min

bot.infinity_polling()
