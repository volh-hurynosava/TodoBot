import telebot
import pandas as pd
from config import TOKEN
bot = telebot.TeleBot(TOKEN)
columns = ['user_id', 'list_index', 'task']
user_list = pd.DataFrame({'user_id': [], 'list_index': [], 'task': []})


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, f'Здравствуй, {message.from_user.first_name}')


@bot.message_handler(commands=['new_item'])
def new_handler(message):
    bot.send_message(message.from_user.id, 'Укажите новый пункт плана')
    bot.register_next_step_handler(message, get_task)
def get_task(message):
    global user_list
    new_task = message.text
    new_index = 1
    if user_list.empty:
        user_list = user_list.append({'user_id': message.from_user.id, 'list_index': new_index, 'task': new_task}, ignore_index=True)
        bot.send_message(message.from_user.id, message.text)
    elif not user_list['user_id'].isin([message.from_user.id]).sum():
        user_list = user_list.append({'user_id': message.from_user.id, 'list_index': new_index, 'task': new_task}, ignore_index=True)
        bot.send_message(message.from_user.id,message.text)
    else:
        new_index = user_list[user_list['user_id'] == message.from_user.id]['list_index'].max() + 1
        user_list = user_list.append({'user_id':message.from_user.id, 'list_index': new_index, 'task': new_task}, ignore_index=True)
        bot.send_message(message.from_user.id,message.text)
@bot.message_handler(commands=['all'])
def all_handler(message):
    global user_list
    if user_list.empty:
        bot.send_message(message.from_user.id, 'Ваш список пуст')
    elif not user_list['user_id'].isin([message.from_user.id]).sum():
        bot.send_message(message.from_user.id, 'Ваш список пуст')
        bot.send_message(message.from_user.id, 'Код красный')
    else:
       bot.send_message(message.from_user.id, user_list[user_list['user_id'] == message.from_user.id].to_string(columns=['list_index','task'], index=False, header=False, line_width=70, justify='left'))
@bot.message_handler(commands=['delete'])
def old_handler(message):
    bot.send_message(message.from_user.id, 'Укажите номер плана для удаления')
    bot.register_next_step_handler(message, get_num)
def get_num(message):
    global user_list
    old_num =float(message.text)
    if user_list.empty:
        bot.send_message(message.from_user.id, 'Список пуст')
    else:
        user_list = user_list.loc[user_list['user_id'] == message.from_user.id ,user_list['list_index'] != old_num ]
        bot.send_message(message.from_user.id,'Сделяль')
bot.polling()