import telebot as tbot
import openpyxl as xl
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests as r
import time

api_token = "7693781694:AAGMuB6q3w2FEZV90IWo5DHYz8ZhJCihBvo"
bot = tbot.TeleBot(api_token)

current_version = "Krivoy(NS)_1.0_Release" 

options = Options()
options.add_argument('--headless=chrome')

def xlsx_search(file, message):
    xlsx = xl.open(f"{file}", read_only=True)
    sheet = xlsx.worksheets[4]

    cell = 20

    raspisanie = f'{sheet["A1"].value} (9К класс): \n \n'
    for i in range (6):
        raspisanie += f'{sheet[f"B{cell}"].value} | {sheet[f'G{cell}'].value}\n'    
        cell += 2
    bot.send_message(message.chat.id, raspisanie) 
    cell = 20
    

def xlsx_export(EXPORT_FORMAT, url):
    output_name = "raspisanie"
    doc_id = url.replace("https://docs.google.com/spreadsheets/d/", "").split("/")[0]

    schedule_url = f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format={EXPORT_FORMAT}'
    response = r.get(schedule_url)

    with open(f'{output_name}.{EXPORT_FORMAT}', 'wb') as f:
        f.write(response.content)
        print(f"Данные успешно скачаны в {output_name}.{EXPORT_FORMAT}")

def url_finder():
    try:
        school_url = "https://sh-kompleks-pokrovskij-r04.gosweb.gosuslugi.ru/glavnoe/raspisanie/"
        print("url ready")

        driver = wd.Chrome(options=options)
        print("driver setted up")

        driver.get(school_url)
        print("window ready")
        time.sleep(1)

        schedule_link = driver.find_element(By.XPATH, '//*[@id="nc-block-df2d29ef0c9d7787f110009fa1561d60"]/div[2]/article/h3[2]/a[2]')
        xlsx_sc = schedule_link.get_attribute('href') 
        print(f"schedule_link contant next - {xlsx_sc}")

        xlsx_export('xlsx', xlsx_sc)
    except Exception as e:
        print('error: ', e)
    finally:
        driver.close()
        driver.quit()
        print("driver closed")

@bot.message_handler(commands=['r'])
def rasp(message):
    xlsx_search("raspisanie.xlsx", message)
    print(f"{message.from_user.username} использовал команду '/r'!")
@bot.message_handler(commands=['ver'])
def ver(message):
    bot.send_message(message.chat.id, f'Текущая версия бота - {current_version}')

def main():
    url_finder()
    bot.polling()

if __name__ == "__main__":
    print("init")
    main()