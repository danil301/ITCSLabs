import telebot, psycopg2, datetime
from telebot import types

conn = psycopg2.connect(database="subjects",
                        user="postgres",
                        password="3012",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


token = "6181520243:AAEkJz7JuPXpdFIQlBTUmYXyqtz8AnO3h3g"

bot = telebot.TeleBot(token)

week = int(datetime.datetime.utcnow().isocalendar()[1]) % 2
if week == 0: next_week = 1
else: next_week = 0



@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Расписание на текущую неделю", "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Бот с расписанием МТУСИ', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, '/mtuci - ссылка на сайт \n'
                                      'Выберите день или неделю, с нужным вам расписанием.')

@bot.message_handler(commands=['week'])
def start_message(message):
    if week == 0:
        bot.send_message(message.chat.id, 'Четная неделя')
    else:
        bot.send_message(message.chat.id, 'Нечетная неделя')

@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')

@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text.lower() == 'понедельник':
        Output("'Понедельник'", message, week)
    elif message.text.lower() == 'вторник':
        Output("'Вторник'", message, week)
    elif message.text.lower() == 'среда':
        Output("'Среда'", message, week)
    elif message.text.lower() == 'четверг':
        Output("'Четверг'", message, week)
    elif message.text.lower() == 'пятница':
        Output("'Пятница'", message, week)
    elif message.text.lower() == 'расписание на текущую неделю':
        week_Output(week, message)
    elif message.text.lower() == 'расписание на следующую неделю':
        week_Output(next_week, message)
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')
    





def Output(day, message, week):
    cursor.execute(
        "SELECT day, subject_name, room_numb, start_time, end_time, full_name FROM timetable INNER JOIN subject on timetable.subject = subject.id INNER JOIN teacher on teacher.subject = subject.id WHERE day=" + str(day) + " AND week='"+str(week)+"'" + "ORDER BY start_time")
    records = list(cursor.fetchall())
    #print(records)
    bot.send_message(message.chat.id, records[0][0])
    bot.send_message(message.chat.id, "-------------------------------------------")
    for i in records:
        line = i[1] + "    " + i[2] + "    " + str(i[3]) + "-" + str(i[4]) + "    " + i[5]
        bot.send_message(message.chat.id, line)
    bot.send_message(message.chat.id, "-------------------------------------------")

def week_Output(week, message):
    cursor.execute(
        "SELECT day, subject_name, room_numb, start_time, end_time, full_name FROM timetable INNER JOIN subject on timetable.subject = subject.id INNER JOIN teacher on teacher.subject = subject.id WHERE week=" + str(
            week))
    records = list(cursor.fetchall())
    print(records)
    for i in records:
        if i[0] == "Понедельник":
            Output("'Понедельник'", message, week)
            break
    for i in records:
        if i[0] == "Вторник":
            Output("'Вторник'", message, week)
            break
    for i in records:
        if i[0] == "Среда":
            Output("'Среда'", message, week)
            break
    for i in records:
        if i[0] == "Четверг":
            Output("'Четверг'", message, week)
            break
    for i in records:
        if i[0] == "Пятница":
            Output("'Пятница'", message, week)
            break


bot.polling(none_stop = True, interval = 0)
