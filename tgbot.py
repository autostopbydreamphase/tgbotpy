import config
import telebot
from telebot import types
from telebot import util

bot = telebot.TeleBot(token = config.token)

@bot.message_handler(commands=['start'])
def start_message(message):

	#keyboard 1
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("help")
	item2 = types.KeyboardButton("Предстоящие матчи")
	markup.add(item2,item1)

	bot.send_message(message.chat.id,text = "Привет, <b>{0.first_name}</b>!\nЯ - <b>{1.first_name}</b>, бот созданный для предоставления информации о будущих матчах,\nвыберите один из вариантов действий снизу.".format(message.from_user,bot.get_me()),
		parse_mode='html',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def inline_data_message(message): 
	if(message.text.lower()=="предстоящие матчи"):
		bot.send_message(message.chat.id,"1")
	elif(message.text.lower()=="help"):
		bot.send_message(message.chat.id,"2")
	else:

		#keyboard 2
		markup = types.InlineKeyboardMarkup(row_width=2)
		item3 = types.InlineKeyboardButton("Предстоящие матчи", callback_data='match')
		item4 = types.InlineKeyboardButton("help", callback_data='help')
		markup.add(item3,item4)

		bot.send_message(message.chat.id, "Я не понимаю, что вы хотите, выберите 1 из кнопок снизу.",reply_markup=markup)
#@bot.message_handler(content_types=['text'])
bot.polling(none_stop=True)