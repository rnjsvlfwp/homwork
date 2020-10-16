import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'};
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers);

raw_data = BeautifulSoup(data.text, 'html.parser');
# print(raw_data)

song_data = raw_data.select('#body-content > div.newest-list > div > table > tbody > tr');
# print(song_data)

for a_song_data in song_data:
    a_song_rank = a_song_data.select_one('td.number').text[0:2].strip();
    a_song_name = a_song_data.select_one('td.info > a.title.ellipsis').text.strip();
    a_song_artist = a_song_data.select_one('td.info > a.artist.ellipsis').text.strip();

    music_data = {
        'rank': a_song_rank,
        'name': a_song_name,
        'artist(s)': a_song_artist
    };

    db.musics.insert_one(music_data);
