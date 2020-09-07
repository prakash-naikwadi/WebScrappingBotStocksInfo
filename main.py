import requests
from bs4 import BeautifulSoup
import csv
import time
import send_mail
from datetime import date

today = str(date.today()) + ".csv"

urls = ["https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch", "https://finance.yahoo.com/quote/GOOG?p=GOOG&.tsrc=fin-srch", "https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch"]

print("----------------------------------------------")

header_titles = ["StockName", "CurrentPrice", "Previous Close", "Open", "Bid", "Ask", "Day's Range", "52 Week Range", "Volume", "Avg. Volume"]


csv_file = open(today, "w")
obj = csv.writer(csv_file)

obj.writerow(header_titles)

for url in urls:
    stock = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}

    html_page = requests.get(url, headers=headers)

    soup = BeautifulSoup(html_page.content, "lxml")

    header_info = soup.find_all("div", id="quote-header-info")[0]
    stock_title = header_info.find("h1", class_="D(ib) Fz(18px)").get_text()

    stock_current_price_info = header_info.find_all("div", class_="D(ib) Mend(20px)")[0].find("span").get_text()
    stock.append(stock_title)
    stock.append(stock_current_price_info)

    class_table = "D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)"
    table_info = soup.find_all("div", class_=class_table)[0].find_all("tr")

    for table_content in table_info:

        value = table_content.find_all("td")[1].get_text()
        stock.append(value)
    obj.writerow(stock)

    time.sleep(5)

print("Data Extraction Completed")

csv_file.close()

send_mail.send(filename=today)
