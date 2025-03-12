#кто смотрит исходник тот лох

# 2хх-коды.
# Коды из этой группы означают, что запрос принят и обработан сервером без ошибок:

# 200 OK — запрос выполнен успешно. Чаще всего встречается именно это число.
# 201 Created — в результате запроса был создан новый ресурс. Как правило, этим кодом отвечают на POST- и иногда PUT-запросы.
# 202 Accepted — запрос принят, но ещё не выполнен. Используется, когда по какой-то причине сервер не может выполнить его сразу. Например, если обработку делает какой-то сторонний процесс, который выполняется раз в день.
# 204 No Content — указывает, что тело ответа пустое, но заголовки могут содержать полезную информацию. Не используется с методом HEAD, поскольку ответ на него всегда должен быть пустым.
# 3хх-коды.
# Это группа кодов перенаправления. Это значит, что клиенту нужно сделать какое-то действие, чтобы запрос продолжил выполняться:

# 301 Moved Permanently — URL запрашиваемого ресурса изменился, новый URL содержится в ответе.
# 302 Found — аналогичен предыдущему коду. Отличие в том, что URL изменился временно. При этом статусе состояния поисковые системы не будут менять ссылку в своей поисковой выдаче на новую.
# 304 Not Modified — означает, что содержимое ресурса было закешировано, его содержимое не поменялось и запрос можно не продолжать.
# 4хх-коды.
# Это коды ошибок, которые допустил клиент при формировании запроса:

# 400 Bad Request — запрос сформирован с ошибкой, поэтому сервер не может его обработать. Причин может быть много, но чаще всего ошибку надо искать в теле запроса.
# 401 Unauthorized — для продолжения необходимо залогиниться.
# 403 Forbidden — пользователь залогинен, но у него нет прав для доступа к ресурсу.
# 404 Not Found — всем известный код: страница не найдена. Некоторые сайты могут возвращать 404 вместо 403, чтобы скрыть информацию от неавторизованных пользователей.
# 405 Method Not Allowed — данный ресурс не поддерживает метод запроса. Например, так бывает, если разработчик хочет отправить PUT-запрос на ресурс, который его не поддерживает.
# 429 Too Many Requests — означает, что сработал защитный механизм: он ограничивает слишком частые запросы от одного пользователя. Таким образом защищаются от DDoS- или brute-force-атак.
# 5хх-коды.
# Это ошибки, которые возникли на сервере во время выполнения запроса:

# 500 Internal Server Error — на сервере произошла неожиданная ошибка. Как правило, происходит из-за того, что в коде сервера возникает исключение.
# 502 Bad Gateway — возникает, если на сервере используеся обратный прокси, который не смог достучаться до приложения.
# 503 Service Unavailable — сервер пока не готов обработать запрос. В ответе также может содержаться информация о том, когда сервис станет доступен.
# 504 Gateway Timeout — эта ошибка означает, что обратный прокси не смог получить ответ за отведенное время (обычно — 60 секунд).

import telebot as tbot
import openpyxl as xl # сокращение
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests as r
import time

#чщщщщщ
api_token = "7693781694:AAGMuB6q3w2FEZV90IWo5DHYz8ZhJCihBvo"
bot = tbot.TeleBot(api_token)

current_version = "Krivoy(NS)_1.0_Release" #NS-NotStable

options = Options()
options.add_argument('--headless=chrome')

def xlsx_search(file, message):
    xlsx = xl.open(f"{file}", read_only=True)
    sheet = xlsx.worksheets[4]# 9-ые квассы

    cell = 20

    #потом чрз цикл для оптимизации и возможности других классов
    raspisanie = f'{sheet["A1"].value} (9К класс): \n \n'
    for i in range (6):
        raspisanie += f'{sheet[f"B{cell}"].value} | {sheet[f'G{cell}'].value}\n'    
        cell += 2
    bot.send_message(message.chat.id, raspisanie) 
    cell = 20
    #дебуг уээ
    # print(f'{sheet["A1"].value} (9К класс)')
    # print(f"{sheet['B20'].value} | {sheet['G20'].value}")
    # print(f"{sheet['B22'].value} | {sheet['G22'].value}")
    # print(f"{sheet['B24'].value} | {sheet['G24'].value}")
    # print(f"{sheet['B26'].value} | {sheet['G26'].value}")
    # print(f"{sheet['B28'].value} | {sheet['G28'].value}")
    # print(f"{sheet['B30'].value} | {sheet['G30'].value}")
    # print(f"{sheet['B32'].value} | {sheet['G32'].value}")

#экспорт таблицы с сайтассылки
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
        time.sleep(1)#микро пауза

        schedule_link = driver.find_element(By.XPATH, '//*[@id="nc-block-df2d29ef0c9d7787f110009fa1561d60"]/div[2]/article/h3[2]/a[2]')#пипиряу чикиряу чо каво
        xlsx_sc = schedule_link.get_attribute('href') #содержимое, крч ссылка
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

    

#чозабретто
if __name__ == "__main__":
    print("init")
    main()