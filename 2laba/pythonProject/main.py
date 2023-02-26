import requests

s_city = 'San Francisco, US'
appid = "9c85842ac398ccdb76f2277a325504c4"

res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()

print("Прогноз погоды на неделю:")

for i in data['list']:
    print("Дата <", i['dt_txt'], "> \r\nСкорость ветра <", i['wind']['speed'], "> \r\nВидимость <", i['visibility'],
          ">")
    print("____________________________")

