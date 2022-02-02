import json
import time
import telebot
import requests
from bs4 import BeautifulSoup
import fake_useragent
import threading
import re
from pytube import YouTube
import string
import random

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
		all_joykes = BeautifulSoup(responce, 'lxml').find_all('div', class_='holder')
		
		for joyk in all_joykes:
			joyk_text = joyk.find('p').text
			for channel in configs['anekdoty']['CHANNEL_LOGIN']:
				bot.send_message(chat_id=channel, text=joyk_text)
				print(f'Joyk added successfully №{a}, page = {page}')
				a += 1
				time.sleep(3600)
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
				time.sleep(3600)
		page += 1

def kulinaria():
	global page
	global added_content
	a = added_content
	while True:
		domain = f"https://www.povarenok.ru/video/~{page}/"
		responce = requests.get(domain, headers=header).text
		recipes = BeautifulSoup(responce, 'lxml').find_all('article', class_='item-bl')

		for recipe in recipes:
			link = recipe.find('a').get('href')
			if link != '#':
				recipe = requests.get(link).text
				recipe_video = BeautifulSoup(recipe, 'lxml').find('div', class_='video-bl').find('iframe').get('src')
				recipe_header = BeautifulSoup(recipe, 'lxml').find('h1').text
				recipe_texts = BeautifulSoup(recipe, 'lxml').find('div', itemtype='http://data-vocabulary.org/Recipe').find_all('div', class_='cooking-bl')
				texts = []
				if recipe_texts != '#':
					for recipe_text in recipe_texts:
						text = recipe_text.find('p').text
						texts.append(text)
				if not texts:
					text = BeautifulSoup(recipe, 'lxml').find('div', itemtype='http://data-vocabulary.org/Recipe').find_all('div')[9].text
					texts.append(text)
				recipe_ingredients = BeautifulSoup(recipe, 'lxml').find('div', class_='ingredients-bl').find_all('li')
				ingridients = []
				for recipe_ingredient in recipe_ingredients:
					ingridient = re.sub("\\s+", ' ', recipe_ingredient.text)
					ingridients.append(ingridient)
				#Dowload youtube video
				video = YouTube(recipe_video).streams.get_highest_resolution().download(output_path='C:\\my\\Telebot', filename='video.mp4')
				for channel in configs['stickers']['CHANNEL_LOGIN']:
					bot.send_video(channel, open('C:\\my\\Telebot\\video.mp4', 'rb'), caption=recipe_header + "\n" + "\n".join(ingridients) + "\n\n" + "\n".join(texts))
					print(f'Recipe added successfully №{a}, page = {page}')
					a += 1
					time.sleep(3)
		page += 1
			

def main():
	#p1 = threading.Thread(target = anekdoty).start()
	#p2 = threading.Thread(target = best_wallpapers).start()
	p3 = threading.Thread(target = kulinaria).start()
	#p1.join()
	#p2.join()
	#p3.join()


if __name__ == "__main__":
	main()
	
	
