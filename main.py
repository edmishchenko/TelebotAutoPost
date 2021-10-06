import json
import time
import telebot
import requests
from bs4 import BeautifulSoup
import fake_useragent


def anekdoty(url):
	pass

def main():
	#USE FAKE-USERAGENT
	user = fake_useragent.UserAgent().random

	#CHANGE HEADER
	header = {'user-agent': user}

	with open("config.json") as file:
	    config = json.load(file)

	anekdoty("https://anekdoty.ru/newjokes/page/{page}/")


if __name__ == "__main__":
	main()