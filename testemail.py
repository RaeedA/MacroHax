import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from selenium.webdriver.common.by import By
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector

def sendemail(html, email):
	sender_email = "testerboi421@gmail.com"
	receiver_email = "testerboi421+" + email
	message = MIMEMultipart("alternative")
	message["Subject"] = "multipart test"
	message["From"] = sender_email
	message["To"] = receiver_email
	message.attach(MIMEText(html, "html"))
#	message.attach(MIMEText(html, "plain"))
	server = smtplib.SMTP_SSL("smtp.gmail.com")
	server.login(sender_email, "password12!")
	server.sendmail(sender_email, receiver_email, message.as_string())
	server.quit()

def find(asin):
	options = Options()
	options.headless = True
	driver = webdriver.Chrome(chrome_options=options)
	driver.get("https://www.amazon.com/dp/" + asin)
#	instock = driver.find_element_by_id("availability")
	instock = driver.find_element_by_xpath("//*[@id=\"availability\"]/span")
	stock = instock.text
	driver.close()
	driver.quit()	
	return stock
	
def getdata():
	cnx1 = mysql.connector.connect(user='root', password='H4ppy:)!',host='localhost',database='macrohacks')
        cnx2 = mysql.connector.connect(user='root', password='H4ppy:)!',host='localhost',database='macrohacks')
	cursor1 = cnx1.cursor()
	cursor2 = cnx2.cursor()
	cursor1.execute("SELECT iD, username, email FROM userinfo")
	info = []

	for (iD, username, email) in cursor1:
		text = ""
		changed = []
		cursor2.execute("SELECT productname, asin, instock FROM productinfo WHERE userid = " + str(iD))
		for (productname, asin, instock) in cursor2:
			iNstock = False
			if(instock == 1):
				iNstock = True
			result = find(asin).lower()
		 	inStock = (("in stock" in result) and not ("on" in result))
			if(inStock != iNstock):
				changed.append(
					{
					"product" : productname,
					"instock" : inStock,
					"asin" : asin
					}
				)
		for i in changed: 
			product = i["product"]
			instock = i["instock"]
			text = text + "\n"
			text = text + "<div>\r\n\t\t<div style=\"display: flex; margin-bottom: -30px;\">\r\n\t\t\t<img src=\""
			src = ""
			stock = ""
			if(instock):
				stock = product + " is in stock!<br>Get it from <a href = \"https://amazon.com/dp/" + i["asin"] + "\">here</a>!"
			else:
				stock = product + " is not in stock!"
			text = text + src + "\" alt=\"\" style=\"margin-top: 10px; height: 3%; width: 3%;\">\r\n\t\t<p style=\"font-size: 20px; margin-left: 3%;\">" + stock + "</p>\r\n\t\t</div>\r\n\t</div>"
			if(not (i in info)):
				info.append(i)

		if(text):
			text = "<html lang=\"en\">\r\n<body style=\"font-family: 'Gill Sans', sans-serif;\">\r\n\t<h1 style=\"text-align: center; font-weight: normal;\">Hey, " + username + "!</h1>\r\n\t" + text + "\r\n</body>\r\n</html>"
			sendemail(text, email)

	for i in info:
                product = i["product"]
                instock = i["instock"]
		inStock = 0
		if(instock):
			inStock = 1
		cursor1.execute("UPDATE productinfo SET instock = " + str(inStock) + " WHERE productname = \"" +  product + "\"")
		cnx1.commit()
	cursor1.close()
	cursor2.close()
	cnx1.close()
	cnx2.close()

getdata()
#sendemail(find("B074CRK54X"));
#print(find("B074CRK54X"))
