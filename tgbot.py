import config
import telebot
from bs4 import BeautifulSoup
import requests
from requests import get
from telebot import types
#from telebot import util

#parser#---------------------------------------------------------------------------------

#URL = 'https://www.hltv.org/matches'
URL1 = 'https://dota2.ru/esport/matches/'
reqs = requests.get(config.URL)
soup = BeautifulSoup(reqs.text,'lxml')

c=[line.getText()for line in soup.find_all('div',class_='matchTeams text-ellipsis')]#список-парсер для названия команд, которые играют
cd=[line.getText()for line in soup.find_all('div',class_='matchTime')]#список-парсер для игрового времени
cdd=[line.getText()for line in soup.find_all('div',class_='matchEventName gtSmartphone-only')]#список-парсер для игрового турнира

reqs1=requests.get(URL1)
soup=BeautifulSoup(reqs1.text,'lxml')

d=[line.getText()for line in soup.find_all('p',class_='cybersport-matches__matches-name')]
dt=[line.getText()for line in soup.find_all('div',class_='time')]

slovarb={1:'/start  - команда для запуска/презапуска бота, т.е. бот начинает своё функционирование с самого начала\nэто равнозначно перезапуску бота.',2:'/help - команда, предоставляющая информацию о сути бота и его функционале.\nИнформация обновляется каждый раз при выходе новой версии бота.',3:'/match - команда, позволяющая получить информацию о ближайших матчах на неделю.\nЯвляется основой командой бота.'}

#Bot#------------------------------------------------------------------------------------

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

		#markup 8
		markup8 = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
		item81 = types.KeyboardButton('Counter-Strike:Global Offensive')
		item82 = types.KeyboardButton('Dota 2')
		markup8.add(item82,item81)
		
		bot.send_message(message.chat.id,'Выберите дисциплину, по которой вы хотите получить матчи.',parse_mode='html', reply_markup=markup8)

	elif(message.text.lower() == 'counter-strike:global offensive'):

		i=0
		while i<len(c):# or i<len(cd) or i<len(cdd):
			bot.send_message(message.chat.id,'GMT+1 '+str(cd[i].replace('\n',' '))+'   |'+str(c[i].replace('\n',' '))+"|   "+str(cdd[i].replace('\n',' ')))
			i+=1

		#keyboard 9
		markup9 = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item19 = types.KeyboardButton('Help')
		item29 = types.KeyboardButton('Предстоящие матчи')
		markup9.add(item29,item19)

		bot.send_message(message.chat.id,'Для справки: время в Беларуси GMT+3.\nТ.е. нужно прибавить +2 часа к времени начала матча.\n<b>LIVE</b> - обозначает, что матч уже идет в live-доступе.\nВсе матчи идут по порядку.',parse_mode='html')
		bot.send_message(message.chat.id,'Для продолжение работы с ботом выберите кнопку снизу или перезапустите',reply_markup=markup9)

	elif(message.text.lower() == 'dota 2'):
		dt2=0
		dtt=0

		#keyboard 10
		markup10 = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item10 = types.KeyboardButton('Help')
		item10 = types.KeyboardButton('Предстоящие матчи')
		markup10.add(item10,item10)

		while dt2<len(dt)-1:
			bot.send_message(message.chat.id,str(dt[dtt].replace('Ч',' ч'))+' | '+str(d[dt2])+' vs '+str(d[dt2+1]))
			dt2+=2
			dtt+=1
		bot.send_message(message.chat.id,'Для продолжение работы с ботом выберите кнопку снизу или перезапустите',reply_markup=markup10)

	elif(message.text.lower()=='help' or message.text.lower()=='/help'):

	#keyboard 1
		markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
		item11 = types.KeyboardButton('Суть бота (если не понятна)')
		item21 = types.KeyboardButton('Документация по командам')
		markup1.add(item11,item21)

		bot.send_message(message.chat.id,text = '<b>Выберите снизу кнопку для дальнейшей работы.</b>',parse_mode='html',reply_markup=markup1)

	elif (message.text.lower()=='суть бота (если не понятна)'):

	#keyboard 4
		markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item14 = types.KeyboardButton('Help')
		item24 = types.KeyboardButton('Предстоящие матчи')
		markup4.add(item24,item14)

		bot.send_message(message.chat.id,'Я - <b>{0.first_name}</b>, бот созданный для предоставления информации о предстоящих матчах.\n\n'.format(bot.get_me()),parse_mode='html',reply_markup=markup4)

	elif (message.text.lower()=='документация по командам'):

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
			item1 = types.KeyboardButton('Суть бота (если не понятна)')
			item2 = types.KeyboardButton('Документация по командам')
			markup.add(item1,item2)

			bot.send_message(call.message.chat.id,text = '<b>Выберите снизу кнопку для дальнейшей работы.</b>',parse_mode='html',reply_markup=markup)

		elif(call.data == 'match'):

			i=0
			while i<len(c):# or i<len(cd) or i<len(cdd):
				bot.send_message(call.message.chat.id,'GMT+1 '+str(cd[i].replace('\n',' '))+'   |'+str(c[i].replace('\n',' '))+"|   "+str(cdd[i].replace('\n',' ')))
				i+=1
			bot.send_message(call.message.chat.id,'Для справки: время в Беларуси GMT+3.\nТ.е. нужно прибавить +2 часа к времени начала матча.\n<b>LIVE</b> - обозначает, что матч уже идет в live-доступе.\nВсе матчи идут по порядку.',parse_mode='html')

		elif(call.data == 'back'):

		#keyboard 5
			markup5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item15 = types.KeyboardButton('Help')
			item25 = types.KeyboardButton('Предстоящие матчи')
			markup5.add(item25,item15)

			bot.send_message(call.message.chat.id,text = '<b>Выберите снизу кнопку для дальнейшей работы.</b>',parse_mode='html',reply_markup=markup5)
		
		elif(call.data == 'next'):

			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите 1 из кнопок снизу.', reply_markup=None)
			b=2

			#keyboard 6
			markup6 = types.InlineKeyboardMarkup(row_width=2)
			item16=types.InlineKeyboardButton('следующая команда',callback_data='next1')
			item26=types.InlineKeyboardButton('вернуться в меню',callback_data='back')
			markup6.add(item16,item26)

			bot.send_message(call.message.chat.id,slovarb[b],parse_mode='html', reply_markup=markup6)

		elif(call.data == 'next1'):

			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите 1 из кнопок снизу.', reply_markup=None)
			b=3

			#keyboard 7
			markup7 = types.InlineKeyboardMarkup(row_width=2)
			item17=types.InlineKeyboardButton('следующая команда',callback_data='next')
			item27=types.InlineKeyboardButton('вернуться в меню',callback_data='back')
			markup7.add(item17,item27)

			bot.send_message(call.message.chat.id,slovarb[b],parse_mode='html', reply_markup=markup7)

		else:
		    # удаление inline кнопок, в сообщении "Я не понимаю, что вы хотите, выберите 1 из кнопок снизу."
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Я не понимаю что вы хотите, выберите 1 из кнопок снизу.', reply_markup=None)

		# надо обновить клавиатуру, чтобы после полученной информации кнопки снизу менялись на обычные
		# при ответе на Предстоящие матчи кнопки должны менятся на что-то соответсвующее (например: выбор вида спорта)
		# (можно использовать обычное добавление клавиатуры к пустому сообщению) - нельзя сделать пустое сообщение...

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