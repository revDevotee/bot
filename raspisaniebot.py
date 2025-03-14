
import telebot as tbot
import openpyxl as xl
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests as r
import time
import datetime

# -*- coding: utf-8 -*-

api_token = "7693781694:AAGMuB6q3w2FEZV90IWo5DHYz8ZhJCihBvo"
bot = tbot.TeleBot(api_token)

#next ver idea - AeroDinahu
current_version = "IUseArchBtw(NS)_1.6_Beta.Linux" 

curr_date = datetime.datetime.today() + datetime.timedelta(days=1)
next_day = curr_date.strftime(f'%d.%m')

#fix site plsplspslpsl
school_site = "https://pokrovsky.gosuslugi.ru"
driver_locate = "/usr/bin/"

#rasp_locate = "/root/rasp_bot/bot/rasp.xlsx"
#changelogs_locate = "/root/rasp_bot/bot/changelogs.txt"
rasp_locate = "C:/Timesword Dev/bot/rspbot/rasp.xlsx"
changelogs_locate = "C:/Timesword Dev/bot/rspbot/changelogs.txt"

options = Options()
#options.add_argument('--headless=chrome')
options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--disable-gpu')
#options.add_argument(f'--user-data-dir={driver_locate}')

def xlsx_search(file, message):
    xlsx = xl.open(f"{file}", read_only=True)
    sheet = xlsx.worksheets[4]

    cell = 20

    #later add multi classes(prob)
    raspisanie = f'{sheet["A1"].value} (9К класс): \n \n'
    for i in range (7):
        raspisanie += f'{cell_check(sheet, cell, "B")} | {cell_check(sheet, cell, "G")}  {cell_check(sheet, cell, "H")}\n'    
        cell += 2
    bot.send_message(message.chat.id, raspisanie) 
    cell = 20

#holy fuck
def cell_check(sheet, cell, letter):
    if sheet[f'{letter}{cell}'].value == None:
        if sheet[f'{letter}{cell + 1}'].value == None:
            if letter == "G":
                return "Урок отсутствует"
            if letter == "H":
                return ""
        else:
            return sheet[f'{letter}{cell + 1}'].value
    else:
        return sheet[f'{letter}{cell}'].value

def xlsx_export(EXPORT_FORMAT, url):
    output_name = "rasp"
    doc_id = url.replace("https://docs.google.com/spreadsheets/d/", "").split("/")[0]

    schedule_url = f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format={EXPORT_FORMAT}'
    response = r.get(schedule_url)
    print("url responsed!")

    #fix
    #kill it with fire
    #redact this path in linux!!!!
    with open(f'{rasp_locate}', 'wb') as f:
        print("Trying to write file")
        f.write(response.content)
        print(f"{output_name}.{EXPORT_FORMAT} successfully ")

def url_finder():
    try:
        #dalshe boga net!
        #driver setup
        print("url ready")
        driver = wd.Chrome(options=options)
        print("driver ready, preparing window")       
        driver.get(school_site)
        print("window ready")
        #fuck that shit
        driver.execute_script("window.scrollBy(0, 12331)")
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/footer/div/div[1]/div/div[3]/ul/li[1]/a').click()
        time.sleep(1)

        #getting xlsx
        schedule_link = driver.find_element(By.XPATH, '//*[@id="nc-block-df2d29ef0c9d7787f110009fa1561d60"]/div[2]/article/h3[2]/a[2]')
        if schedule_link.text.replace("Изменения в расписании старшей школы на ", "") != next_day:
            schedule_link = driver.find_element(By.XPATH, '//*[@id="nc-block-df2d29ef0c9d7787f110009fa1561d60"]/div[2]/article/h3[2]/a[3]')
        xlsx_sc = schedule_link.get_attribute('href') 
        print(f"schedule_link contant next - {xlsx_sc}")

        xlsx_export('xlsx', xlsx_sc)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
        driver.quit()
        print("driver closed")

@bot.message_handler(commands=['r'])
def rasp(message):
    xlsx_search({rasp_locate}, message)
    print(f"{message.from_user.username} used command '/r'!")
@bot.message_handler(commands=['ver'])
def ver(message):
    bot.send_message(message.chat.id, f'Текущая версия бота - {current_version}')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Перед использованием бота, прочитайте <a href='https://telegra.ph/Polzovatelskoe-soglashenie-dlya-ispolzovaniya-bota-raspisaniervdvtbot-03-12'>пользовательское соглашение/политику конфиденциальности!</a>", parse_mode='HTML')
@bot.message_handler(commands=['changelogs'])
def bot_updates(message):
    msg = ""
    with open(changelogs_locate, "r", encoding='utf-8') as file:
        for line in file:
            msg += f'{line}\n'
    bot.send_message(message.chat.id, f"Список изменений: \n{msg}")
    msg = ""
@bot.message_handler(commands=['updatedata'])
def data_update(message):
    url_finder()

def main():
    url_finder()
    print(f"{bot.user.username} ready")
    bot.infinity_polling()
    

if __name__ == "__main__":
    print("init")
    main()
