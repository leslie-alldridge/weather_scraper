import requests
import pandas
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email import message, encoders
from bs4 import BeautifulSoup

from env import secret

# Email globals
from_addr = 'trademe102@windowslive.com'
to_addr = 'leslie.alldridge@gmail.com'
subject = 'The latest weather in Wellington'

# URL request
page=requests.get("https://weather.com/en-IN/weather/tenday/l/db888870838d6b522ca125ca2bfedd033ff8ae4ba4e1c90bfc8c0f4e44abb2f5")
content=page.content
soup=BeautifulSoup(content,"html.parser")

# Data array we want to fill
data = []

all=soup.find("div",{"class":"locations-title ten-day-page-title"}).find("h1").text
 
table=soup.find_all("table",{"class":"twc-table"})
for items in table:
	for i in range(len(items.find_all("tr"))-1):
		d = {}
		try:
			d["day"]=items.find_all("span",{"class":"date-time"})[i].text
			d["date"]=items.find_all("span",{"class":"day-detail"})[i].text			
			d["desc"]=items.find_all("td",{"class":"description"})[i].text
			d["temp"]=items.find_all("td",{"class":"temp"})[i].text
			d["precip"]=items.find_all("td",{"class":"precip"})[i].text
			d["wind"]=items.find_all("td",{"class":"wind"})[i].text
			d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text
		except:
			d["day"]="None"
			d["date"]="None"
			d["desc"]="None"
			d["temp"]="None"
			d["precip"]="None"
			d["wind"]="None"
			d["humidity"]="None"
		data.append(d)

df = pandas.DataFrame(data)
# Export as html table
df.to_html('weather.html')	

# Open the file we've made
html = open("weather.html")
msg = MIMEText(html.read(), 'html')

# Create email
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject

server = smtplib.SMTP('smtp.live.com', 587)
server.connect("smtp.live.com", 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(from_addr, secret)
# Stringify msg
msg = msg.as_string()

server.sendmail(from_addr, to_addr, msg)