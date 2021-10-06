import json
import time
import telebot
import requests
from bs4 import BeautifulSoup
import fake_useragent

#USE FAKE-USERAGENT
user = fake_useragent.UserAgent().random

#CHANGE HEADER
header = {'user-agent': user}

with open("config.json") as file:
    configs = json.load(file)

page = 1
added_joyk_count = 1
bot = telebot.TeleBot(configs['API_TOKEN'])

def anekdoty(page):
	timeOfMsg = 1633503840
	global added_joyk_count
	domain = f"https://anekdoty.ru/newjokes/page/{page}/"
	responce = requests.get(domain, headers=header).text
	all_joykes = BeautifulSoup(responce, 'lxml').find_all('div', class_='text-holder')

	for joyk in all_joykes:
	    for channel in configs['anekdoty']['CHANNEL_LOGIN']:
	        bot.send_message(chat_id=channel, text=joyk.text, schedule_date=timeOfMsg)
	        print(f'Joyk added successfully №{added_joyk_count}')
	        added_joyk_count += 1
	        

def best_wallpapers(page):
	timeOfMsg = 1633503840
	domain = f"https://wallpaperscraft.com/all/page{page}"
	responce = requests.get(domain, headers=header).text
	images = BeautifulSoup(responce, 'lxml').find_all('li', class_='wallpapers__item')
	for image in images:
		link = image.find('img').get('src').replace('300x168', '1280x720')
		for channel in configs['best_wallpapers']['CHANNEL_LOGIN']:
			bot.send_photo(chat_id=channel, photo=link, schedule_date=timeOfMsg)
			bot.send_document(chat_id=channel, filename=link, schedule_date=timeOfMsg)

def main():
#Need to add loop
	global page
	#anekdoty(page)
	best_wallpapers(page)
	#Increment page of site
	page += 1

if __name__ == "__main__":
	main()
