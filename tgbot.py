import config
import telebot
from bs4 import BeautifulSoup
import requests  #библиотека нужна для парсинга ,нужно ли импортировать библиотеку? или можно просто из неё импортировать то, что нам надо?...
from requests import get
from telebot import types
#from telebot import util

#parser

#URL = 'https://www.hltv.org/matches'
reqs = requests.get(config.URL)
soup = BeautifulSoup(reqs.text,'lxml')
c=[line.getText()for line in soup.find_all('div',class_='matchTeams text-ellipsis')]


slovarb={1:'/start  - команда для запуска/презапуска бота, т.е. бот начинает своё функционирование с самого начала\nэто равнозначно перезапуску бота.',2:'/help - команда, предоставляющая информацию о сути бота и его функционале.\nИнформация обновляется каждый раз при выходе новой версии бота.',3:'/match - команда, позволяющая получить информацию о ближайших матчах на неделю.\nЯвляется основой командой бота.'}


bot = telebot.TeleBot(token = config.token)

@bot.message_handler(commands=['start'])  #start, отправляет сообщение с картинкой по адресу
def start_message(message):

	#keyboard 1
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton('Help')
	item2 = types.KeyboardButton('Предстоящие матчи')
	markup.add(item2,item1)

	bot.send_photo(message.chat.id, get('https://i.pinimg.com/564x/3f/22/e3/3f22e3170ce6eca2d6ecf121f191bf9f.jpg').content) #.content, чтобы получить конкретно картинку, а не список байтов по запросу
	bot.send_message(message.chat.id,text = 'Привет, <b>{0.first_name}</b>!\nЯ - <b>{1.first_name}</b>, бот созданный для предоставления информации о предстоящих матчах,\nвыберите один из вариантов действий снизу.'.format(message.from_user,bot.get_me()),
		parse_mode='html',reply_markup=markup)


@bot.message_handler(content_types=['text'])  #ответ на сообщения button'ov
def inline_data_message(message): 

	if(message.text.lower()=='предстоящие матчи' or message.text.lower()=='match' or message.text.lower()=='/match'):
		i=0
		while i<len(c):
			bot.send_message(message.chat.id,str(c[i].replace('\n',' ')))
			i+=1

	elif(message.text.lower()=='help' or message.text.lower()=='/help'):
		markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
		item11 = types.KeyboardButton('Суть бота (если не понятна).')
		item21 = types.KeyboardButton('Документация по командам.')
		markup1.add(item11,item21)

		bot.send_message(message.chat.id,text = '<b>Выберите снизу кнопку для дальнейшей работы.</b>',parse_mode='html',reply_markup=markup1)



	elif (message.text.lower()=='суть бота (если не понятна).'):

	#keyboard 4
		markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item14 = types.KeyboardButton('Help')
		item24 = types.KeyboardButton('Предстоящие матчи')
		markup4.add(item24,item14)

		bot.send_message(message.chat.id,'Я - <b>{0.first_name}</b>, бот созданный для предоставления информации о предстоящих матчах.\n\n'.format(bot.get_me()),
		parse_mode='html',reply_markup=markup4)

	elif (message.text.lower()=='документация по командам.'):  ####ALLOO######

	#keyboard 6
		markup6 = types.InlineKeyboardMarkup(row_width=2)
		item16=types.InlineKeyboardButton('следующая команда',callback_data='next')
		item26=types.InlineKeyboardButton('вернуться в меню',callback_data='back')
		markup6.add(item16,item26)
		i=1
		bot.send_message(message.chat.id,slovarb[i],parse_mode='html', reply_markup=markup6)
	
	else:

		#keyboard 2
		markup = types.InlineKeyboardMarkup(row_width=2)
		item3 = types.InlineKeyboardButton('Предстоящие матчи', callback_data='match')
		item4 = types.InlineKeyboardButton('Help', callback_data='help')
		markup.add(item3,item4)

		bot.send_message(message.chat.id, 'Я не понимаю, что вы хотите, выберите 1 из кнопок снизу.',reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)  #ответ на вызов inline button'ov #ф-ция lambda служит для првоерки сообщения, если лямбда возвращает True, сообщение обрабатывается декорированной функцией, чтобы все сообщения обрабатывались этой функцией, мы просто всегда возвращаем True
def callback_inline(call):
	if call.message:

		if (call.data == 'help'):

			#keyboard 3
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
			item1 = types.KeyboardButton('Суть бота (если не понятна).')
			item2 = types.KeyboardButton('Документация по командам.')
			markup.add(item1,item2)

			bot.send_message(call.message.chat.id,text = '<b>Выберите снизу кнопку для дальнейшей работы.</b>',parse_mode='html',reply_markup=markup)

		elif(call.data == 'match'):
			i=0
			while i<len(c):
				bot.send_message(call.message.chat.id,str(c[i].replace('\n',' ')))
				i+=1

		elif(call.data == 'back'):

		#keyboard 5
			markup5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item15 = types.KeyboardButton('Help')
			item25 = types.KeyboardButton('Предстоящие матчи')
			markup5.add(item25,item15)
			bot.send_message(call.message.chat.id,text = '<b>Выберите снизу кнопку для дальнейшей работы.</b>',parse_mode='html',reply_markup=markup5)

		elif(call.data == 'next'):
			b=2
			if(b<4):

		#keyboard 6
				markup6 = types.InlineKeyboardMarkup(row_width=2)
				item16=types.InlineKeyboardButton('следующая команда',callback_data='next')
				item26=types.InlineKeyboardButton('вернуться в меню',callback_data='back')
				markup6.add(item16,item26)

				bot.send_message(call.message.chat.id,slovarb[b],parse_mode='html', reply_markup=markup6)
				b+=1
		# удаление inline кнопок, в сообщении "Я не понимаю, что вы хотите, выберите 1 из кнопок снизу."
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Я не понимаю что вы хотите, выберите 1 из кнопок снизу.', reply_markup=None)

		# надо обновить клавиатуру, чтобы после полученной информации кнопки снизу менялись на обычные
		# при ответе на Предстоящие матчи кнопки должны менятся на что-то соответсвующее (например: выбор вида спорта)
		# (можно использовать обычное добавление клавиатуры к пустому сообщению)

#	@bot.message_handler(func=lambda c:True, content_types=['text'])#этот блок выполнится если юзер отправит боту сообщение
#	def info_message(message):
#		bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')# удаляем кнопки у последнего сообщения

#inline keyboard 3
#markup=types.InlineKeyboardMarkup(row_width=2)
#item1=types.InlineKeyboardButton("Суть бота (если не понятна).",callback_data='func')
#item2=types.InlineKeyboardButton("Документация по командам.",callback_data='doc')	

#@bot.message_handler(commands=['start'])
#@bot.message_handler(content_types=['text'])
#@bot.callback_query_handler(func=lambda call: True)


bot.polling(none_stop=True)