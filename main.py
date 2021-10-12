import json
import time
import telebot
import requests
from bs4 import BeautifulSoup
import fake_useragent
import threading

#USE FAKE-USERAGENT
user = fake_useragent.UserAgent().random

#CHANGE HEADER
header = {'user-agent': user}

with open("config.json") as file:
    configs = json.load(file)

page = 1
added_content = 1
bot = telebot.TeleBot(configs['API_TOKEN'])

def anekdoty():
	global added_content 
	a = added_content
	global page
	while True:
		domain = f"https://anekdoty.ru/newjokes/page/{page}/"
		responce = requests.get(domain, headers=header).text
		all_joykes = BeautifulSoup(responce, 'lxml').find_all('div', class_='text-holder')

		for joyk in all_joykes:
		    for channel in configs['anekdoty']['CHANNEL_LOGIN']:
		        bot.send_message(chat_id=channel, text=joyk.text)
		        print(f'Joyk added successfully №{a}, page = {page}')
		        a += 1
		        time.sleep(60)
		page += 1

def best_wallpapers():
	global page
	global added_content
	a = added_content
	while True:
		domain = f"https://wallpaperscraft.com/all/page{page}"
		responce = requests.get(domain, headers=header).text
		images = BeautifulSoup(responce, 'lxml').find_all('li', class_='wallpapers__item')
		for image in images:
			link = image.find('img').get('src').replace('300x168', '1280x720')
			for channel in configs['best_wallpapers']['CHANNEL_LOGIN']:
				bot.send_photo(chat_id=channel, photo=link)
				bot.send_document(channel, link)
				print(f'Image added successfully №{a}, page = {page}')
				a += 1
				time.sleep(60)
		page += 1

def main():
	p1 = threading.Thread(target = anekdoty)
	p2 = threading.Thread(target = best_wallpapers)
	p1.start()
	p2.start()
	p1.join()
	p2.join()


if __name__ == "__main__":
	main()
	
	
