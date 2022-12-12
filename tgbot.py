import config
import telebot
from bs4 import BeautifulSoup
import requests  #библиотека нужна для парсинга ,нужно ли импортировать библиотеку? или можно просто из неё импортировать то, что нам надо?...
from requests import get
from telebot import types
from telebot import util

bot = telebot.TeleBot(token = config.token)

@bot.message_handler(commands=['start'])  #start, отправляет сообщение с картинкой по адресу
def start_message(message):

	#keyboard 1
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("help")
	item2 = types.KeyboardButton("Предстоящие матчи")
	markup.add(item2,item1)

	bot.send_photo(message.chat.id, get("https://i.pinimg.com/564x/3f/22/e3/3f22e3170ce6eca2d6ecf121f191bf9f.jpg").content) #.content, чтобы получить конкретно картинку, а не список байтов по запросу
	bot.send_message(message.chat.id,text = "Привет, <b>{0.first_name}</b>!\nЯ - <b>{1.first_name}</b>, бот созданный для предоставления информации о будущих матчах,\nвыберите один из вариантов действий снизу.".format(message.from_user,bot.get_me()),
		parse_mode='html',reply_markup=markup)


@bot.message_handler(content_types=['text'])  #ответ на сообщения button'ov
def inline_data_message(message): 

	if(message.text.lower()=="предстоящие матчи"):
		bot.send_message(message.chat.id,"в дальнейшей доработке")
	
	elif(message.text.lower()=="help"):
		markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
		item11 = types.KeyboardButton("Суть бота (если не понятна).")
		item21 = types.KeyboardButton("Документация по командам.")
		markup1.add(item11,item21)

		bot.send_message(message.chat.id,text = "<b>Выберите снизу кнопку для дальнейшей работы.</b>",parse_mode='html',reply_markup=markup1)
	elif (message.text.lower()=="суть бота (если не понятна)."):
		bot.send_message(message.chat.id,"Я - <b>{0.first_name}</b>, бот созданный для предоставления информации о будущих матчах.\n\n".format(bot.get_me()),
		parse_mode='html')

	else:

		#keyboard 2
		markup = types.InlineKeyboardMarkup(row_width=2)
		item3 = types.InlineKeyboardButton("Предстоящие матчи", callback_data='match')
		item4 = types.InlineKeyboardButton("help", callback_data='help')
		markup.add(item3,item4)

		bot.send_message(message.chat.id, "Я не понимаю, что вы хотите, выберите 1 из кнопок снизу.",reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)  #ответ на вызов inline button'ov #ф-ция lambda служит для првоерки сообщения, если лямбда возвращает True, сообщение обрабатывается декорированной функцией, чтобы все сообщения обрабатывались этой функцией, мы просто всегда возвращаем True
def callback_inline(call):
	if call.message:

		if (call.data == 'help'):
			
			kortezh=() #надо добавить какой-то кортеж (возможно будет в каждом элементе картежа - 1 функция бота)

			#keyboard 3
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
			item1 = types.KeyboardButton("Суть бота (если не понятна).")
			item2 = types.KeyboardButton("Документация по командам.")
			markup.add(item1,item2)

			bot.send_message(call.message.chat.id,text = "<b>Выберите снизу кнопку для дальнейшей работы.</b>",parse_mode='html',reply_markup=markup)

		elif(call.data == 'match'):
			bot.send_message(call.message.chat.id,'///')

        # удаление inline кнопок, в сообщении "Я не понимаю, что вы хотите, выберите 1 из кнопок снизу."
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Я не понимаю, что вы хотите, выберите 1 из кнопок снизу.", 
            reply_markup=None)
		# надо обновить клавиатуру, чтобы после полученной информации кнопки снизу менялись на обычные
		# при ответе на Предстоящие матчи кнопки должны менятся на что-то соответсвующее (например: выбор вида спорта)
		# (можно использовать обычное добавление клавиатуры к пустому сообщению)

#inline keyboard 3
#markup=types.InlineKeyboardMarkup(row_width=2)
#item1=types.InlineKeyboardButton("Суть бота (если не понятна).",callback_data='func')
#item2=types.InlineKeyboardButton("Документация по командам.",callback_data='doc')	

#@bot.message_handler(commands=['start'])
#@bot.message_handler(content_types=['text'])
#@bot.callback_query_handler(func=lambda call: True)

bot.polling(none_stop=True)