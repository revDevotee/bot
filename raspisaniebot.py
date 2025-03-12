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

from datetime import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests as r
import time
import re
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless')

EXPORT_FORMAT = 'xlsx'#формат экспорта таблицы


def Main():
    try:
        school_url = "https://sh-kompleks-pokrovskij-r04.gosweb.gosuslugi.ru/glavnoe/raspisanie/"
        print("url ready")

        driver = wd.Chrome()
        print("driver setted up")

        driver.get(school_url)
        print("window ready")
        time.sleep(2)

        #БЛЯТЬ УРАААААААА, С 63 И 64 СТРОКА ВОЙДУТ В ЮБИЛЕЙНЫЕ СТРОКИ
        schedule_link = driver.find_element(By.XPATH, '//*[@id="nc-block-df2d29ef0c9d7787f110009fa1561d60"]/div[2]/article/h3[2]/a[3]')
        xlsx_sc = schedule_link.get_attribute('href') #containtment of schelude_link
        print(f"schedule_link contant next - {xlsx_sc}")
        
        url = "https://docs.google.com/spreadsheets/d/1WhCpZaaugZ8WhLtbWM71Q6TrRM_oXkhD/edit?gid=963336423#gid=963336423"

        doc_id = url.replace("https://docs.google.com/spreadsheets/d/", "").split("/")[0]

        schedule_url = f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format={EXPORT_FORMAT}'
        response = r.get(schedule_url)

        with open(f'output.{EXPORT_FORMAT}', 'wb') as f:
            f.write(response.content)
            print(f"Данные успешно скачаны в output.{EXPORT_FORMAT}")
       
        time.sleep(10)
    except Exception as e:
        print('error: ', e)
    finally:
        driver.close()
        driver.quit()
        print("driver closed")

if __name__ == "__main__":
    print("init")
    Main()