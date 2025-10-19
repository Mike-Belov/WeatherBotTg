from selenium import webdriver
import time
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import telebot
from telebot import types
from datetime import datetime
from threading import Thread
import schedule

#запускаем поток для отправки каждые час температуры
def Time(message): 
    schedule.every().hour.at(2).do(message)
    print("Таймер запущен")
    message(message)
    countert = 0
    while True:
        countert +=1
        print(countert)
        schedule.run_pending()
        time.sleep(1)

#Заголовки для парсинга
def init_webdriver():
    driver = webdriver.Chrome() 
    stealth(driver, 
            platform="Win32",
            vendor="Google Inc.",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine")
    return driver

def message(message):
    bot.send_message(message.chat.id, temperaturatwohour())

def temperaturatwohour():
    global soup
    temperaturatoday=soup.find("span", class_="AppFactTemperature_sign__1MeN4 AppFactTemperature_attr__8pcxc").text
    temperaturatoday1 =soup.find("span", class_="AppFactTemperature_value__2qhsG").text
    pogoda = 'Сейчас температура {}'.format(temperaturatoday)
    pogoda+=temperaturatoday1
    return pogoda

def parsingpogoda(numberday):
    global soup
    day=soup.find_all("h3", style="grid-area:day-title")[numberday].text
    temperaturamoning = soup.find_all("div", style="grid-area:m-temp")[numberday].text
    temperaturaday = soup.find_all("div", style="grid-area:d-temp")[numberday].text
    temperaturaevening = soup.find_all("div", style="grid-area:d-temp")[numberday].text
    temperaturanight = soup.find_all("div", style="grid-area:n-temp")[numberday].text
    
    pogodamoning = soup.find_all("div", style="grid-area:m-text")[numberday].text
    pogodaday = soup.find_all("div", style="grid-area:d-text")[numberday].text
    pogodaevening = soup.find_all("div", style="grid-area:e-text")[numberday].text
    pogodanight = soup.find_all("div", style="grid-area:n-text")[numberday].text

    pogoda = "{}".format(day) +"\nУтром {}".format(temperaturamoning)+" ({}".format(pogodamoning)+")\nДнем {}".format(temperaturaday)+" ({}".format(pogodaday)+")\nВечером {}".format(temperaturaevening)+" ({}".format(pogodaevening)+")\nНочью {}".format(temperaturanight)+" ({}".format(pogodanight)+")" 
    return pogoda

def error(message):
    print("Ошибка")
    bot.send_message(message.chat.id, "Произошла ошибка подключения😢! \nНе переживайте наша команда уже трудиться")

def Weekday(numberweekday):
    if numberweekday == 0:
        day = "ПОГОДА В ПОНЕДЕЛЬНИК"
    elif numberweekday == 1:
        day = "ПОГОДА ВО ВТОРНИК"
    elif numberweekday == 2:
        day = "ПОГОДА В СРЕДУ"
    elif numberweekday == 3:
        day = "ПОГОДА В ЧЕТВЕРГ"
    elif numberweekday == 4:
        day = "ПОГОДА В ПЯТНИЦУ"
    elif numberweekday == 5:
        day = "ПОГОДА В СУББОТУ" 
    elif numberweekday == 6:
        day = "ПОГОДА В ВОСКРЕСЕНЬЕ"    
    else:
        print("Не удалось получить информацию (смотреть день недели (def Weekday))")                       
       
    return day      

url = "https://yandex.ru/pogoda/ru"    
driver = init_webdriver()

#Создание бота ТГ
TOKEN = "8305337492:AAFZF9M5NZndGooGBp44_9reT9uKXcBjf38"
bot = telebot.TeleBot(TOKEN)

print("Бот запущен")  

driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")

#keyboard 
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnToday = types.KeyboardButton(f"ПОГОДА СЕГОДНЯ")
btnInformation = types.KeyboardButton("📃Информация")
btnYesteday = types.KeyboardButton(f"ПОГОДА ЗАВТРА")

#Дни недели
year = int(datetime.now().strftime('%Y'))
month = int(datetime.now().strftime('%m'))

endmonth = 5
newmoth = 0

try:
    yesteday = datetime(year, month, int(datetime.now().strftime('%d'))+1)
except:
    newmoth += 1
try:
    day1 = datetime(year, month, int(datetime.now().strftime('%d'))+2)
except:
    endmonth = endmonth-1
    newmoth += 1
try:
    day2 = datetime(year, month, int(datetime.now().strftime('%d'))+3)
except:
    endmonth = endmonth-1 
    newmoth += 1 
try:
    day3 = datetime(year, month, int(datetime.now().strftime('%d'))+4)
except:
    endmonth = endmonth-1  
    newmoth += 1

markup.add(btnToday, btnYesteday, btnInformation)        

#создаем клавиатуру
for i in range(2, endmonth):
    try:
        daytoday = int(datetime.now().strftime('%d'))+i
        day = datetime(year, month, daytoday)
        day = day.weekday()
    
        btn = types.KeyboardButton(f"{Weekday(day)}")       
        markup.add(btn) 
    except:
        print("Погода будет известна через несколько дней")    

if month+1 > 12:  
    nextmonth = 1
    year = int(datetime.now().strftime('%Y'))+1
else:
    nextmonth = month+1

if newmoth > 0:
    if newmoth == 4:
        day1 = datetime(year, nextmonth, 2)
        day2 = datetime(year, nextmonth, 3)
        day3 = datetime(year, nextmonth, 4)
     
        for i in range(1, 4):
            try:
               daytoday = i+1
               day = datetime(year, nextmonth, daytoday)
               day = day.weekday()

               weatherspeed = 3
            
               btn = types.KeyboardButton(f"({Weekday(day)}")     
               weatherspeed +=1  
               markup.add(btn) 
            except:
               print("Погода будет известна через несколько дней") 
    elif newmoth == 3:
        day1 = datetime(year, nextmonth+1, 1)
        day2 = datetime(year, nextmonth+1, 2)
        day3 = datetime(year, nextmonth+1, 3)

        for i in range(1, 4):
            try:
               daytoday = i
               day = datetime(year, nextmonth, daytoday)
               day = day.weekday()

               weatherspeed = 3
            
               btn = types.KeyboardButton(f"{Weekday(day)}")     
               weatherspeed += 1  
               markup.add(btn) 
            except:
               print("Погода будет известна через несколько дней") 
    elif newmoth == 2:
        day2 = datetime(year, nextmonth, 1)
        day3 = datetime(year, nextmonth, 2)

        for i in range(1, 3):
            try:
               daytoday = i
               day = datetime(year, nextmonth, daytoday)
               day = day.weekday()

               weatherspeed = 4
            
               btn = types.KeyboardButton(f"{Weekday(day)}")  
               weatherspeed +=1     
               markup.add(btn) 
            except:
               print("Погода будет известна через несколько дней") 
    elif newmoth == 1:
        day3 = datetime(year, nextmonth, 1) 
        try:
           daytoday = 1
           day = datetime(year, nextmonth, daytoday)
           day = day.weekday()
        
           btn = types.KeyboardButton(f"{Weekday(day)}")       
           markup.add(btn) 
        except:
           print("Погода будет известна через несколько дней")         
    
#обработчики комад
@bot.message_handler(commands=['start'])
def Hello(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}🤪. Меня зовут {1.first_name}. Если хочешь узнать погоду нажми кнопку ПОГОДА, выбрав день".
                     format(message.from_user, bot.get_me()), reply_markup=markup)
    #второй поток
    #th = Thread(target=Time(message))
    #th.start()
    
@bot.message_handler(content_types=['text'])
def Weather(message):
    if message.text == f"ПОГОДА СЕГОДНЯ":
        bot.send_message(message.chat.id, parsingpogoda(0))

    elif message.text == "📃Информация":
        bot.send_message(message.chat.id, "Bot создан в развлекательных целях. Вся информация берется с сайта " + 
                         f"https://yandex.ru/pogoda/ . Телеграмм  bot с открытым исходным кодом. Ссылка на GitHub " + 
                         f"https://github.com/Mike-Belov/TelegramWeather. По всем вопросам @MikiBelov")         
        
    elif message.text == f"ПОГОДА ЗАВТРА":
        bot.send_message(message.chat.id,parsingpogoda(1))
    elif message.text == f"{Weekday(day1.weekday())}":
        bot.send_message(message.chat.id,parsingpogoda(2))

    elif message.text == f"{Weekday(day2.weekday())}":
        bot.send_message(message.chat.id,parsingpogoda(3))
    elif message.text == f"{Weekday(day3.weekday())}":        
       bot.send_message(message.chat.id,parsingpogoda(4))
    else:
        bot.send_message(message.chat.id, "Не понял вас😩. Повторите")     


while True:
    try:
        bot.polling(none_stop=True,timeout=5)
    except Exception as e:
        print(e)