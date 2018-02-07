from bs4 import BeautifulSoup
import requests
import re
from tkinter import *

searchurl = "https://search.azlyrics.com/search.php?q="
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
song = 'default'

def convert_string(name):
    name = list(name)
    res = []
    for emt in name:
        if emt == ' ':
            res.append('+')
            continue
        res.append(str(emt.lower()))
    res = "".join(res)
    return res

def create_txt(lyricsinlistform, songname, artistname):
    f = open(artistname + ' - ' + songname + '.txt', 'w')
    f.write("\n".join(lyricsinlistform).strip())
    f.close

def return_lyrics(link):
    response = requests.get(link, headers = headers)
    html = response.content
    link = list(link)
    songname = []
    artistname = []
    while link[len(link) - 1] != '.':
        link.pop()
    link.pop()
    while link[len(link) - 1] != '/':
        songname.append(link.pop())
    songname = "".join(songname[::-1])
    link.pop()
    while link[len(link) - 1] != '/':
        artistname.append(link.pop())
    artistname ="".join(artistname[::-1])
    soup = BeautifulSoup(html, "lxml")
    lyrics = soup.find_all('div', attrs = {'class': None, 'id': None})
    lyrics = [x.getText() for x in lyrics]
    create_txt(lyrics, songname, artistname)

def search(name):
    generate_url = searchurl + convert_string(name)
    response = requests.get(generate_url)
    html = response.content

    soup = BeautifulSoup(html, "lxml")
    reallink = soup.find('td', attrs = {"class": "text-left visitedlyr", "id": None })
    try:
        dest_link = str(reallink.find('a', href = re.compile('^https://www.azlyrics.com/lyrics/'))['href'])
        return_lyrics(dest_link)
    except AttributeError:
        print("Error Searching")
    except TypeError:
        print("Error Searching")


