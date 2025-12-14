from selenium import webdriver
import time
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import telebot
from telebot import types
from datetime import datetime
from threading import Thread
import schedule
from TOKEN import *

#запускаем поток для отправки каждые 3 часа температуры после нажатия кнопки start
def Time(message): 
    print("Таймер запущен")
    while True:
        Message(message)
        time.sleep(10800)

#Заголовки для парсинга
def init_webdriver():
    driver = webdriver.Chrome() 
    stealth(driver, 
            platform="Win32",
            vendor="Google Inc.",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine")
    return driver

#функция для создания клавиатуры
def keyboard():
    global day1, day2, day3

    #keyboard 
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
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
    return(markup)              

def twokeyboard(message):
    new_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    new_keyboard.add('Подробнее', "Назад")
    
    # Обновляем меню, отправляя новое сообщение с новой клавиатурой
    bot.send_message(message.chat.id, 'Хотите узнать подробнее?', reply_markup=new_keyboard) 

def Message(message):
    bot.send_message(message.chat.id, temperaturahour())

def KeyboardMessage(message, markup):
    bot.send_message(message.chat.id, "", reply_markup=markup)

#Для обновления клавиатуры в 00:01 (3 поток)
def KeyboardTime(message):
    if schedule.every().day.at("00:01").do():
        markup=keyboard()
        KeyboardMessage(message, markup)
    while True:
        schedule.run_pending()
        time.sleep(1)

#Температура сейчас(каждыне 3 часа)
def temperaturahour():
    global soup
    temperaturatoday=soup.find("span", class_="AppFactTemperature_sign__1MeN4 AppFactTemperature_attr__8pcxc").text
    temperaturatoday1 =soup.find("span", class_="AppFactTemperature_value__2qhsG").text
    weather =soup.find("p", class_="AppFact_warning__8kUUn").text
    pogoda = 'Сейчас температура {}'.format(temperaturatoday)+"{}".format(temperaturatoday1)+"\n{}".format(weather)
    return pogoda

#Парсим погоду
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

    pogoda = ("{}".format(day) +"\nУтром {}".format(temperaturamoning)+" ({}".format(pogodamoning)+")\nДнем {}".format(temperaturaday)+
    " ({}".format(pogodaday)+")\nВечером {}".format(temperaturaevening)+" ({}".format(pogodaevening)+")\nНочью {}".format(temperaturanight)+" ({}".format(pogodanight)+")")
    return pogoda

#Подробный парсинк
def detailedparsink():
    global soup, numberday
    
    windmoning = soup.find_all("div", style="grid-area:m-wind")[numberday].text
    windday = soup.find_all("div", style="grid-area:d-wind")[numberday].text
    windevening = soup.find_all("div", style="grid-area:e-wind")[numberday].text
    windnight = soup.find_all("div", style="grid-area:n-wind")[numberday].text

    directionmoning = soup.find_all("div", style="grid-area:m-dir")[numberday].text
    directionday = soup.find_all("div", style="grid-area:d-dir")[numberday].text
    directionevening = soup.find_all("div", style="grid-area:e-dir")[numberday].text
    directionnight = soup.find_all("div", style="grid-area:n-dir")[numberday].text

    humiditymoning = soup.find_all("div", style="grid-area:m-hum")[numberday].text
    humidityday = soup.find_all("div", style="grid-area:d-hum")[numberday].text   
    humidityevening = soup.find_all("div", style="grid-area:e-hum")[numberday].text
    humiditynight = soup.find_all("div", style="grid-area:n-hum")[numberday].text

    pressuremoning = soup.find_all("div", style="grid-area:m-press")[numberday].text
    pressureday = soup.find_all("div", style="grid-area:d-press")[numberday].text
    pressureevening = soup.find_all("div", style="grid-area:e-press")[numberday].text
    pressurenight = soup.find_all("div", style="grid-area:n-press")[numberday].text

    pogoda = (f"Ветер м/с \t Влажность \t Давление мм.рт.ст\nУтром \t\t{windmoning} \t{directionmoning} \t\t\t\t{humiditymoning} \t\t\t\t{pressuremoning}"+
    f"\nДнем \t\t{windday} \t{directionday} \t\t\t\t{humidityday} \t\t\t\t{pressureday}"+
    f"\nВечером \t\t{windevening} \t{directionevening} \t\t\t\t{humidityevening} \t\t\t\t{pressureevening}"+
    f"\nНочью \t\t{windnight} \t{directionnight} \t\t\t\t{humiditynight} \t\t\t\t{pressurenight}") 
    return pogoda

#Обрабатываем ошибки
def error(message):
    print("Ошибка")
    bot.send_message(message.chat.id, "Произошла ошибка подключения😢! \nНе переживайте наша команда уже трудиться")

#Выясняем день недели
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

bot = telebot.TeleBot(TOKEN)

day1= 0
day2 = 0
day3 = 0
numberday = 0

print("Бот запущен")  

driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")    

#обработчики комад
@bot.message_handler(commands=['start'])
def Hello(message):
    markup=keyboard()
    if message.text == '/start':
        bot.send_message(message.chat.id, "Привет, {0.first_name}🤪. Меня зовут {1.first_name}. Если хочешь узнать погоду нажми кнопку ПОГОДА, выбрав день".
                     format(message.from_user, bot.get_me()), reply_markup=markup)
        #второй поток
        th2 = Thread(target=Time(message))
        th2.start()
        #третий поток
        th3 = Thread(target=KeyboardTime(message))
        th3.start()
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Выберите день", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Выберите еще какой-нибудь день", reply_markup=markup)    
    
@bot.message_handler(content_types=['text'])
def Weather(message):
    global numberday
    markup = keyboard()
    if message.text == "ПОГОДА СЕГОДНЯ":
        bot.send_message(message.chat.id, parsingpogoda(0))
        numberday = 0
        twokeyboard(message)

    elif message.text == "📃Информация":
        bot.send_message(message.chat.id, "Bot создан в развлекательных целях. Вся информация берется с сайта " + 
                         f"https://yandex.ru/pogoda/ . Телеграмм  bot с открытым исходным кодом. Ссылка на GitHub " + 
                         f"https://github.com/Mike-Belov/WeatherBotTg. По всем вопросам @MikiBelov", reply_markup=markup)         
        
    elif message.text == "ПОГОДА ЗАВТРА":
        bot.send_message(message.chat.id,parsingpogoda(1))
        numberday = 1
        twokeyboard(message)
    elif message.text == f"{Weekday(day1.weekday())}":
        bot.send_message(message.chat.id,parsingpogoda(2))
        numberday = 2
        twokeyboard(message)

    elif message.text == f"{Weekday(day2.weekday())}":
        bot.send_message(message.chat.id,parsingpogoda(3))
        numberday = 3
        twokeyboard(message)
    elif message.text == f"{Weekday(day3.weekday())}":        
        bot.send_message(message.chat.id,parsingpogoda(4))
        numberday = 4
        twokeyboard(message)

    elif message.text == "Назад":
        Hello(message)

    elif message.text == "Подробнее":
        bot.send_message(message.chat.id, detailedparsink())
        Hello(message)     

    else:
        bot.send_message(message.chat.id, "Не понял вас😩. Повторите. Возможно стоит перезапустить бота")     


#Цикл, чтобы бот не останавливался 
while True:
    try:
        bot.polling(none_stop=True,timeout=5)
    except Exception as e:

        print(e)

