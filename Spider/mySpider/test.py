import requests
from bs4 import BeautifulSoup


play_url='http://www.baidu.com/'

s = requests.session()
s = BeautifulSoup(s.get(play_url).content)
print(s)
main = s.find('ul',{'id','lh'})
print(main)

for music in main.find_all('a'):
    print('{}:{}'.format(music.text,music['href']))