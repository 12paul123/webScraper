import requests
from bs4 import BeautifulSoup
import time, os
import asyncio
import smtplib

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

site = "https://www.blocket.se"
URL_1 = site + "/annonser/hela_sverige/fordon/batar/segelbat?cg=1062"
URL_2 = site + "/annonser/hela_sverige/fritid_hobby/musikutrustning/gitarr_bas_forstarkare?cg=6161"

session = requests.Session()

def init_server():
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

async def send(ad, current_time):
	section = "".join(ad[0]).encode("ascii", "ignore").decode("ascii")
	subject = "Ad Found! {}, {}".format(current_time, section)
	body = "Price: {} URL: {}{}".format(ad[1], site, ad[2])
	msg = f"Subject: {subject}\n\n{body}"

	try:
		server.sendmail(EMAIL_ADDRESS, "opticdragonbf3@gmail.com", msg)
	except Exception as e:
		print(e)
		server.close()

async def parse_site(url):
	page = session.get(url, verify=True)
	soup = BeautifulSoup(page.content, "html.parser")
	return soup

async def get_latest_ad(url):
	soup = await parse_site(url)
	ad_elems = soup.find_all("article", class_="hidZFy")
	latest_ad = ad_elems[0]

	ad_name = latest_ad.find("span", class_ = "jzzuDW").text
	ad_price = latest_ad.find("div", class_ = "jkvRCw").text
	ad_url = latest_ad.find("a", class_="enigRj")["href"]

	return (ad_name, ad_price, ad_url)

async def search_url(url):
	current_ad = await get_latest_ad(url)

	while True:
		ad = await get_latest_ad(url)

		t = time.localtime()
		current_time = time.strftime("%H:%M:%S", t)

		if current_ad[0] == ad[0]:
			await asyncio.sleep(300)
			print("No new ad found... ", current_time)
		else:
			await send(ad, current_time)

async def main():
	coroutines = [search_url(URL_1), search_url(URL_2)]
	await asyncio.gather(*coroutines)

if __name__ == "__main__":
	server = smtplib.SMTP('smtp.gmail.com', 587)
	init_server()

	asyncio.run(main())