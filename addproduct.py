import re
import mysql.connector
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def parse(url):
	return re.search("dp\/(..........)", url).group(1)

def add(url, username):
        cnx1 = mysql.connector.connect(user='api', password='test',host='raeed-hackathon.cjxojia4mlpx.us-west-2.rds.amazonaws.com',database='hackathon')
        cursor1 = cnx1.cursor()
	
	asin = parse(url)

	options = Options()
        options.headless = True
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
	productname = driver.title
	if ("Amazon.com" in productname):
		productname = productname[14:]
	driver.close
	driver.quit
	if(len(productname) >= 100):
		productname = productname[0:99]
	cursor1.execute("INSERT INTO productinfo (userid, productname, asin, instock) VALUES ((SELECT iD from userinfo WHERE username = \"" + str(username) + "\"), \"" + str(productname) + "\", \"" + str(asin) + "\", 0)")
	cnx1.commit()

        cursor1.close()
        cnx1.close()

add(raw_input("URL: "),raw_input("Username: "))
