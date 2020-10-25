import requests
from bs4 import BeautifulSoup
import time, os
import smtplib
import threading
import sys

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

site = "https://www.blocket.se"
URL_1 = site + "/annonser/hela_sverige/fordon/batar/segelbat?cg=1062"
URL_2 = site + "/annonser/hela_sverige/fritid_hobby/musikutrustning/gitarr_bas_forstarkare?cg=6161"
URL_3 = site + "/annonser/sodermanland/fordon/bilar?cg=1020&pe=1&r=12"
session = requests.Session()

def init_server():
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

def send(ad, current_time):
	section = "".join(ad[0]).encode("ascii", "ignore").decode("ascii")
	subject = "Ad Found! {}, {}".format(current_time, section)
	body = "Price: {} URL: {}{}".format(ad[1], site, ad[2])
	msg = f"Subject: {subject}\n\n{body}"

	try:
		server.sendmail(EMAIL_ADDRESS, "opticdragonbf3@gmail.com", msg)
	except Exception as e:
		print(e)
		server.close()
		sys.exit()

def parse_site(url):
	page = session.get(url, verify=True)
	soup = BeautifulSoup(page.content, "html.parser")
	return soup

def get_latest_ad(url):
	soup = parse_site(url)
	ad_elems = soup.find_all("article", class_="hidZFy")
	latest_ad = ad_elems[0]

	ad_name = latest_ad.find("span", class_ = "jzzuDW").text
	ad_price = latest_ad.find("div", class_ = "jkvRCw").text
	ad_url = latest_ad.find("a", class_="enigRj")["href"]

	return (ad_name, ad_price, ad_url)

def search_url(url):
	current_ad = get_latest_ad(url)

	while True:
		ad = get_latest_ad(url)

		t = time.localtime()
		current_time = time.strftime("%H:%M:%S", t)

		if current_ad[0] == ad[0]:
			time.sleep(300)
			print("No new ad found... ", current_time)
		else:
			send(ad, current_time)
			current_ad = ad

if __name__ == "__main__":
	server = smtplib.SMTP('smtp.gmail.com', 587)
	init_server()

	t1 = threading.Thread(target=search_url, args=(URL_1,))
	t2 = threading.Thread(target=search_url, args=(URL_2,))
	t3 = threading.Thread(target=search_url, args=(URL_3,))
	t1.start()
	t2.start()
	t3.start()