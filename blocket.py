import requests
from bs4 import BeautifulSoup
import time
import asyncio

URL_1 = "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062"
URL_2 = "https://www.blocket.se/annonser/hela_sverige/fritid_hobby/musikutrustning/gitarr_bas_forstarkare?cg=6161"
session = requests.Session()

async def parse_site(url):
	page = session.get(url, verify=True)
	soup = BeautifulSoup(page.content, "html.parser")
	return soup

async def get_latest_ad(url):
	soup = await parse_site(url)
	ad_elems = soup.find_all("article", class_="hidZFy")
	latest_ad = ad_elems[0]

	# hitta namn, pris och url
	ad_name = latest_ad.find("span", class_ = "jzzuDW").text
	ad_price = latest_ad.find("div", class_ = "jkvRCw").text
	ad_url = latest_ad.find("a", class_="enigRj")["href"]

	return (ad_name, ad_price, ad_url)

async def search_url(url):
	current_ad = await get_latest_ad(url)

	while True:
		ad = await get_latest_ad(url)
		if current_ad[0] == ad[0]:
			await asyncio.sleep(300)

			t = time.localtime()
			current_time = time.strftime("%H:%M:%S", t)

			print("No new ad found... ", current_time)
		else:
			print("New: ", current_ad[0], "Time: ", current_time)

async def main():
	coroutines = [search_url(URL_1), search_url(URL_2)]
	await asyncio.gather(*coroutines)

asyncio.run(main())