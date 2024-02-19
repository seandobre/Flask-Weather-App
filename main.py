from flask import Flask,request, jsonify,render_template
from bs4 import BeautifulSoup
import requests
import json
import random
app = Flask(__name__)
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
backgrounds = ["https://media.giphy.com/media/13bGgH9VnEDsuA/giphy.gif"," https://th.bing.com/th/id/R.9bbce29878a8dc0411c900aa05f9b3dc?rik=AiWmfL06B8bCzQ&riu=http%3a%2f%2fpsd.fanextra.com%2fwp-content%2fuploads%2f2012%2f04%2fsmokeship6a.jpg&ehk=rogPljYfZcWrlWo5ruquL%2bQACHM7Dv%2fi7Yx2FHk0TKQ%3d&risl=&pid=ImgRaw&r=0", "https://media.giphy.com/media/13bGgH9VnEDsuA/giphy.gif","https://media.giphy.com/media/131A1qWMxETWPm/giphy.gif"]
query = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

def getLocationImages(Loctation,Time):
   url = f'https://www.istockphoto.com/photos/{Loctation} at {Time}'
   page = requests.get(url, headers=header)
   soup = BeautifulSoup(page.text,'html.parser')
   image = soup.find_all(class_='bOaTkZcdqgXxzJCZECTz')
   if len(image) > 3:
       return image[random.randint(0,len(image) -1)]['src']
   else:
      return backgrounds[0]

def getBasic(q):
   url = f'https://www.google.com/search?q=weather+{q}'
   page = requests.get(url, headers=header)
   soup = BeautifulSoup(page.text,'html.parser')
   Region = soup.find('span', class_='BBwThe')
   
   currentWeatherF = soup.find('span', class_='wob_t q8U8x', id='wob_tm')
   currentWeatherC = soup.find('span', id='wob_ttm', class_='wob_t')
   currentWeatherIMG = soup.find('img', id='wob_tci')

   return [Region.get_text(),currentWeatherF.get_text(),currentWeatherC.get_text(),currentWeatherIMG['src']]

@app.route("/")
def Home():
  
   a = getBasic(query[random.randint(0,45)])
   x = getBasic(query[random.randint(0,45)])
   y = getBasic(query[random.randint(0,45)])
   i = getBasic(query[random.randint(0,45)])
   url = f'https://www.google.com/search?q=weather+near+me'
   page = requests.get(url, headers=header)
   soup = BeautifulSoup(page.text,'html.parser')

   Region = soup.find('span', class_='BBwThe')
   currentWeatherF = soup.find('span', class_='wob_t q8U8x', id='wob_tm')
   currentWeatherC = soup.find('span', id='wob_ttm', class_='wob_t')
   currentWeatherIMG = soup.find('img', id='wob_tci')
   Wind = soup.find('div', class_='wtsRwe')
   moreData = [i.get_text().strip() for i in Wind]
   weatherText = soup.find('span',id='wob_dc')
   NextDaysData = soup.find('div', class_='R3Y3ec rr3bxd')
   futureDays = [i.get_text() for i in NextDaysData.findChildren('span',class_='wob_t') if i.text != '']
   futureDays1 = [i.get_text() for i in NextDaysData.findChildren('div',class_='Z1VzSb') if i.text != '']
   Time = soup.find('div',class_='wob_dts')
   return render_template('home.html',a=a, x=x, y=y,i=i,data=[Region.get_text(), currentWeatherF.getText(),currentWeatherC.getText(), currentWeatherIMG['src']], extra=[moreData[0],moreData[1],moreData[2],weatherText], Days=futureDays1, futureWeather=futureDays,time=Time.get_text())

@app.route("/region/<id>")
def get_user(id):
   url = f'https://www.google.com/search?q=weather+{id}'
   page = requests.get(url, headers=header)
   soup = BeautifulSoup(page.text,'html.parser')
   
   Region = soup.find('span', class_='BBwThe')
   currentWeatherF = soup.find('span', class_='wob_t q8U8x', id='wob_tm')
   currentWeatherC = soup.find('span', id='wob_ttm', class_='wob_t')
   currentWeatherIMG = soup.find('img', id='wob_tci')
   Wind = soup.find('div', class_='wtsRwe')
   moreData = [i.get_text().strip() for i in Wind]
   weatherText = soup.find('span',id='wob_dc')
   NextDaysData = soup.find('div', class_='R3Y3ec rr3bxd')
   futureDays = [i.get_text() for i in NextDaysData.findChildren('span',class_='wob_t') if i.text != '']
   futureDays1 = [i.get_text() for i in NextDaysData.findChildren('div',class_='Z1VzSb') if i.text != '']
   Time = soup.find('div',class_='wob_dts')
   bgnum = backgrounds[random.randint(0,3)]
   BackgroundFuction = getLocationImages(Region.get_text(),Time.get_text())
   print("Searched: " + f"https://www.google.com/search?q={Region.get_text()}+at+{Time.get_text()}+Image+Istock")
   print(BackgroundFuction)
   print(futureDays)
   print(futureDays1)
  

   return render_template('index.html',data=[Region.get_text(), currentWeatherF.getText(),currentWeatherC.getText(), currentWeatherIMG['src']], extra=[moreData[0],moreData[1],moreData[2],weatherText], Days=futureDays1, futureWeather=futureDays,time=Time.get_text(),bg=BackgroundFuction)
