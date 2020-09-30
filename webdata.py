
from socket import *
from requests import *
from bs4 import *            #BeautifulSoup
from tkinter import *

def loc():
    try:
        create_connection(("www.google.com",80))
        res = get("https://ipinfo.io")
        print(res)
        data = res.json()            #json is a method to get data fro =m site in form of dictionary
        city = data['city']
        return city
    except Exception as e:
        print("sorry")

def temp():
    api_address = " "
    city = "dombivali"
    create_connection(("www.google.com",80))    #port no to ensure connection
    a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
    a2 = "&q=" + city
    a3 = "&appid=c6e315d09197cec231495138183954bd"
    api_address = a1 + a2 + a3
    res = get(api_address)
    print(res)
    data = res.json()                        #converts web data to list
    print(data)
    temp = data['main']
    temp1 = temp['temp']
    return temp1


def quote():
    text = " "
    res = get("https://www.brainyquote.com/quote_of_the_day")

    soup = BeautifulSoup(res.text,"lxml")
    data = soup.find("img",{"class":"p-qotd"})
    text = data['alt']
    return text

    
    
        	
	
