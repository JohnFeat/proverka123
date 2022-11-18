from tkinter.ttk import Separator
from urllib import request
from peewee import *
import requests
from bs4 import BeautifulSoup
import time
db = SqliteDatabase('data.db')
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import utils
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import re
from config import *

from config import admin_id
import time
print(utils.get_chat_by_id)
otheradmins = 210828253
import gspread
# Указываем путь к JSON
gc = gspread.service_account(filename='arizona-crime-syndicates-b20c695b3c07.json')
print('Connected! [1]')
#Открываем тестовую таблицу
sh = gc.open("Tucson || Мафии ☠")
print('Find a table! [2]')
print(sh.worksheet('Основная таблица').get('A3'))
worksheet = sh.worksheet("Основная таблица")
logsheet = sh.worksheet('Лог выговоров')
lgotsheet = sh.worksheet('Логи льгот')
immunity = sh.worksheet('Иммунитеты')
online = sh.worksheet('Онлайн')
blacklist = sh.worksheet('Чёрный список')
values_list = worksheet.col_values(4)
print(values_list)

class MyLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)
chat_ids = [2]


i = 0
class VkBot:
	def __init__(self):
		self.vk_session = vk_api.VkApi(token=token)
		self.longpoll = MyLongPoll(self.vk_session, 206202169)


	def run(self):
			   
	

		for event in self.longpoll.listen():
			
			if event.type == VkBotEventType.MESSAGE_NEW:
				
				try:
					
					msg = event.object.message
					
					user_id = msg['from_id']
					chat_id = event.chat_id
					user = utils.get_user_by_id(user_id)
					chats = utils.get_chat_by_id(chat_id)

					text = msg['text']
					print(user.nickname,':', text, '[', event.chat_id, ']')

					fwd = self.vk_session.method('messages.getByConversationMessageId', {
					'conversation_message_ids': msg['conversation_message_id'],
					'peer_id': msg['peer_id']
					})['items'][0]
					
					if text[0:6] == '/setlg':
						search = text[7:]
						idf, value, reason = re.findall(r"\[id(\d*)\|@.*] (\d*)\ (.*)", search)[0]
						print(idf, value, reason)
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):

								valcol = lgotsheet.col_values(2)
								a = len(valcol) + 1
								for i in range(len(values_list)):
									if values_list[i] == userf.nickname:
										if i + 1 <= 7:
											fraction = worksheet.get(f'A{i + 1}')[0][0]
											frac_list = worksheet.get(f'L5:O5')[0]
											print(frac_list)

								lgotsheet.update(f'B{a}', int(value))
								lgotsheet.update(f'C{a}', 'Да')
								lgotsheet.update(f'D{a}', reason)
								lgotsheet.update(f'E{a}', user.nickname)
								lgotsheet.update(f'F{a}', worksheet.get('K2'))
								lgotsheet.update(f'A{a}', fraction)
								for i in range(len(frac_list)):
												if frac_list[i] == fraction:
													frac_lgotlist = worksheet.col_values(i + 12)
													print(frac_lgotlist)
								userf.lgoti = frac_lgotlist[12]
								self.vk_session.method('messages.send', {
									'chat_id': 3,
									'message': f'✅ {user.adminstatus} {user.nickname} выдал {userf.nickname} льготы в размере {value} штук. Льготы на данный момент: {userf.lgoti}.',
									'random_id': 0
									})
								self.vk_session.method('messages.send', {
									'chat_id': 1,
									'message': f'✅ {user.adminstatus} {user.nickname} выдал {userf.nickname} льготы в размере {value} штук. Льготы на данный момент: {userf.lgoti}.',
									'random_id': 0
									})
								userf.save()
						else:
							self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Эта команда Вам не доступна.',
								'random_id': 0
								})
					elif text[0:5] == '/unlg':
						search = text[6:]
						idf, value, reason = re.findall(r"\[id(\d*)\|@.*] (\d*)\ (.*)", search)[0]
						print(idf, value, reason)
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):
								valcol = lgotsheet.col_values(2)
								a = len(valcol) + 1
								for i in range(len(values_list)):
									if values_list[i] == userf.nickname:
										if i + 1 <= 7:
											fraction = worksheet.get(f'A{i + 1}')[0][0]
											frac_list = worksheet.get(f'L5:O5')[0]
											print(frac_list)

								lgotsheet.update(f'B{a}', int(value))
								lgotsheet.update(f'C{a}', 'Нет')
								lgotsheet.update(f'D{a}', reason)
								lgotsheet.update(f'E{a}', user.nickname)
								lgotsheet.update(f'F{a}', worksheet.get('K2'))
								lgotsheet.update(f'A{a}', fraction)
								for i in range(len(frac_list)):
												if frac_list[i] == fraction:
													frac_lgotlist = worksheet.col_values(i + 12)
													print(frac_lgotlist)
								userf.lgoti = frac_lgotlist[12]
								self.vk_session.method('messages.send', {
									'chat_id': 3,
									'message': f'✅ {user.adminstatus} {user.nickname} снял {userf.nickname} льготы в размере {value} штук. Льготы на данный момент: {userf.lgoti}.',
									'random_id': 0
									})
								self.vk_session.method('messages.send', {
									'chat_id': 1,
									'message': f'✅ {user.adminstatus} {user.nickname} снял {userf.nickname} льготы в размере {value} штук. Льготы на данный момент: {userf.lgoti}.',
									'random_id': 0
								})
								userf.save()
							else:
								self.vk_session.method('messages.send', {
									'chat_id': msg['peer_id'] - 2000000000,
									'message': f'Эта команда Вам не доступна.',
									'random_id': 0
									})
					if text == '/cmdlist':

							self.vk_session.method('messages.send', {
									'chat_id': msg['peer_id'] - 2000000000,
									'message': f'Список команд бота:\n\nАдминистраторам:\n/setpred - Выдать предупреждение\n/unpred - Снять предупреждение\n/setvig - Выдать выговор\n/unvig - Снять выговор\n/checkstats - Посмотреть статистику /setorg - Установить орг\n/nickname @id "Nick_Name" - Установить ник\n/setstatus - Установить статус (Лидер, Заместитель)\n/kick @id "Причина" - кикнуть пользователя с причиной\n\nЛидерам, Заместителям:\n/mystats - посмотреть свою статистику',
									'random_id': 0
									})

					if text[0:7] == '/setorg':
						search = text[8:]
						idf	 = re.findall(r'\[id(\d*)\|@.*]', search)[0]
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):
								search = text[8:]
								idf, org = re.findall(r'\[id(\d*)\|@.*] (.*)', search)[0]
								user = utils.get_user_by_id(idf)
								user.org = org
								user.save()
								self.vk_session.method('messages.send', {
										'chat_id': msg['peer_id'] - 2000000000,
										'message': f'✅ Игроку {user.nickname} присвоена организация "{user.org}"',
										'random_id': 0
										})
							else:
								self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Нельзя выполнить какие-либо действия с пользователем, выше Вас статусом.',
								'random_id': 0
								})
						else:
							self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Эта команда Вам не доступна.',
								'random_id': 0
								})
					if text[0:10] == '/setstatus':
						search = text[8:]
						idf	 = re.findall(r'\[id(\d*)\|@.*]', search)[0]
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):
								try:
									print('увидел')
									search = text[11:]

									idf, some = re.findall(r'\[id(\d*)\|@(.*)] .*', search)[0]
									user = utils.get_user_by_id(idf)
									adminstatus = re.findall(r'\[id\d*\|@.*] (.*)', search)[0]
									print('adminstatus = ', adminstatus)
									user.adminstatus = adminstatus

									self.vk_session.method('messages.send', {
										'chat_id': msg['peer_id'] - 2000000000,
										'message': f'✅{user.nickname} был выдан статус: {adminstatus}',
										'random_id': 0
										})
									user.save()
									return VkBot().run()
								except:
									self.vk_session.method('messages.send', {
										'chat_id': msg['peer_id'] - 2000000000,
										'message': f'Произошла непредвиденная ошибка!\nВозможно вы ошиблись с ID пользователя, либо он не найден. Повторите попытку.',
										'random_id': 0
									})
									return VkBot().run()
							else:
								self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Нельзя выполнить какие-либо действия с пользователем, выше вас статусом.',
								'random_id': 0
								})
						else:
							self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Эта команда Вам не доступна.',
								'random_id': 0
								})
					if text[0:6] == '/unvig':
						search = text[7:]
						idf	 = re.findall(r'\[id(\d*)\|@.*]', search)[0]
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):
								search = text[7:]
								idf = re.findall(r'\[id(\d*)\|@.*]', search)[0]
								reason = re.findall(r'\[id\d*\|@.*] (.*)', search)[0]
								userf = utils.get_user_by_id(idf)
								valcol = logsheet.col_values(2)
								a = len(valcol) + 1
								for i in range(len(values_list)):
									if values_list[i] == userf.nickname:
										if i + 1 <= 7:
											fraction = worksheet.get(f'A{i + 1}')[0][0]
											frac_list = worksheet.get(f'L5:O5')[0]
											print(frac_list)

								logsheet.update(f'B{a}', 1)
								logsheet.update(f'C{a}', 'Строгий')
								logsheet.update(f'D{a}', 'Нет')
								logsheet.update(f'E{a}', reason)
								logsheet.update(f'F{a}', user.nickname)
								logsheet.update(f'G{a}', worksheet.get('K2'))
								logsheet.update(f'A{a}', fraction)
								for i in range(len(frac_list)):
												if frac_list[i] == fraction:
													frac_viglist = worksheet.col_values(i + 12)
													print(frac_viglist)
								userf.vigs = frac_viglist[5]
								self.vk_session.method('messages.send', {
									'chat_id': 3,
									'message': f'✅ {user.adminstatus} {user.nickname} снял строгий выговор {userf.nickname}. Причина: {reason}. Выговоров на данный момент {userf.vigs}/5.',
									'random_id': 0
									})
								self.vk_session.method('messages.send', {
									'chat_id': 1,
									'message': f'✅ {user.adminstatus} {user.nickname} снял строгий выговор {userf.nickname}. Причина: {reason}. Выговоров на данный момент {userf.vigs}/5.',
									'random_id': 0
								})
								userf.save()
							else:
								self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Нельзя выполнить какие-либо действия с пользователем, выше Вас статусом.',
								'random_id': 0
								})
						else:
							self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Эта команда Вам не доступна.',
								'random_id': 0
								})


					if text[0:7] == '/setvig':
						idf	 = re.findall(r'\[id(\d*)\|@.*]', search)[0]
						userf = utils.get_user_by_id(idf)
						if user.lvladmin >= 2:
							if user.lvladmin >= userf.lvladmin:
								search = text[8:]
								idf = re.findall(r'\[id(\d*)\|@.*]', search)[0]
								reason = re.findall(r'\[id\d*\|@.*] (.*)', search)[0]
								userf = utils.get_user_by_id(idf)
								valcol = logsheet.col_values(2)
								a = len(valcol) + 1
								for i in range(len(values_list)):
									if values_list[i] == userf.nickname:
										if i + 1 <= 7:
											fraction = worksheet.get(f'A{i + 1}')[0][0]
											frac_list = worksheet.get(f'L5:O5')[0]
											print(frac_list)

								logsheet.update(f'B{a}', 1)
								logsheet.update(f'C{a}', 'Строгий')
								logsheet.update(f'D{a}', 'Да')
								logsheet.update(f'E{a}', reason)
								logsheet.update(f'F{a}', user.nickname)
								logsheet.update(f'G{a}', worksheet.get('K2'))
								logsheet.update(f'A{a}', fraction)
								for i in range(len(frac_list)):
												if frac_list[i] == fraction:
													frac_viglist = worksheet.col_values(i + 12)
													print(frac_viglist)
								userf.vigs = frac_viglist[5]
								self.vk_session.method('messages.send', {
									'chat_id': msg['peer_id'] - 2000000000,
									'message': f'✅ {user.adminstatus} {user.nickname} выдал {userf.nickname} строгий выговор. Выговоров на данный момент: {userf.lgoti}/5',
									'random_id': 0
									})
								userf.save()
							else:
								self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Нельзя выполнить какие-либо действия с пользователем, выше Вас статусом.',
								'random_id': 0
								})
						else:
							self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Эта команда Вам не доступна.',
								'random_id': 0
								})
					if text[0:7] == '/unpred':
						search = text[8:]
						idf	 = re.findall(r'\[id(\d*)\|@.*]', search)[0]
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):
								search = text[8:]
								idf = re.findall(r'\[id(\d*)\|@.*]', search)[0]
								reason = re.findall(r'\[id\d*\|@.*] (.*)', search)[0]
								userf = utils.get_user_by_id(idf)
								valcol = logsheet.col_values(2)
								a = len(valcol) + 1
								for i in range(len(values_list)):
									if values_list[i] == userf.nickname:
										if i + 1 <= 7:
											fraction = worksheet.get(f'A{i + 1}')[0][0]
											frac_list = worksheet.get(f'L5:O5')[0]
											print(frac_list)

								logsheet.update(f'B{a}', 1)
								logsheet.update(f'C{a}', 'Устный')
								logsheet.update(f'D{a}', 'Нет')
								logsheet.update(f'E{a}', reason)
								logsheet.update(f'F{a}', user.nickname)
								logsheet.update(f'G{a}', worksheet.get('K2'))
								logsheet.update(f'A{a}', fraction)
								for i in range(len(frac_list)):
												if frac_list[i] == fraction:
													frac_viglist = worksheet.col_values(i + 12)
													print(frac_viglist)
								userf.pred = frac_viglist[6]
								self.vk_session.method('messages.send', {
								'chat_id': 1,
								'message': f'✅ {user.adminstatus} {user.nickname} снял устный выговор {userf.nickname}. Причина: {reason}. Устных выговоров на данный момент {userf.pred}/3.',
								'random_id': 0
								})
								self.vk_session.method('messages.send', {
								'chat_id': 3,
								'message': f'✅ {user.adminstatus} {user.nickname} снял устный выговор {userf.nickname}. Причина: {reason}. Устных выговоров на данный момент {userf.pred}/3.',
								'random_id': 0
								})
								userf.save()
							else:
								self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Нельзя выполнить какие-либо действия с пользователем, выше Вас статусом.',
								'random_id': 0
								})
						else:
							self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Эта команда Вам не доступна.',
								'random_id': 0
								})



					if text[0:8] == '/setpred':
						search = text[9:]
						idf	 = re.findall(r'\[id(\d*)\|@.*]', search)[0]
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):

								search = text[9:]
								idf = re.findall(r'\[id(\d*)\|@.*]', search)[0]
								reason = re.findall(r'\[id\d*\|@.*] (.*)', search)[0]
								userf = utils.get_user_by_id(idf)
								valcol = logsheet.col_values(2)
								a = len(valcol) + 1
								for i in range(len(values_list)):
									if values_list[i] == userf.nickname:
										if i + 1 <= 7:
											fraction = worksheet.get(f'A{i + 1}')[0][0]
											frac_list = worksheet.get(f'L5:O5')[0]
											print(frac_list)

								logsheet.update(f'B{a}', 1)
								logsheet.update(f'C{a}', 'Устный')
								logsheet.update(f'D{a}', 'Да')
								logsheet.update(f'E{a}', reason)
								logsheet.update(f'F{a}', user.nickname)
								logsheet.update(f'G{a}', worksheet.get('K2'))
								logsheet.update(f'A{a}', fraction)
								for i in range(len(frac_list)):
												if frac_list[i] == fraction:
													frac_viglist = worksheet.col_values(i + 12)
													print(frac_viglist)
								userf.pred = frac_viglist[6]
								self.vk_session.method('messages.send', {
								'chat_id': 3,
								'message': f'✅ {user.adminstatus} {user.nickname} выдал устный выговор {userf.nickname}. Причина: {reason}. Устных выговоров на данный момент {userf.pred}/3.',
								'random_id': 0
								})
								self.vk_session.method('messages.send', {
								'chat_id': 1,
								'message': f'✅ {user.adminstatus} {user.nickname} выдал устный выговор {userf.nickname}. Причина: {reason}. Устных выговоров на данный момент {userf.pred}/3.',
								'random_id': 0
								})
								userf.save()
							else:
								self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌Нельзя выполнить какие-либо действия с пользователем, выше Вас статусом.',
								'random_id': 0
								})
						else:
							self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌Эта команда Вам не доступна.',
								'random_id': 0
								})
					if 'reply_message' in fwd:
						fwd = fwd['reply_message']
					else:
						fwd = None
					if text == '!upd':
							if user.lvladmin >= 2:
								chat_id = event.chat_id
								chats = utils.get_chat_by_id(chat_id)
								chats.chatiki = chat_id
								chats.save()
								self.vk_session.method('messages.send', {
									'chat_id': msg['peer_id'] - 2000000000,
									'message': f'Чат внесен в базу данных. Текущий ID чата: [ {chat_id} ] | Уникальный номер чата: {chat_id} ✅',
									'random_id': 0
									})
							else:
								self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌ Эта команда Вам не доступна.',
								'random_id': 0
								})




					if text[0:9] == '/nickname':
						search = text[10:]
						idf	 = re.findall(r'\[id(\d*)\|@.*]', search)[0]
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):
								nick = text[10:]
								idf, nick= re.findall(r'\[id(\d*)\|@.*] (.*)', nick)[0]

								user = utils.get_user_by_id(idf)
								uname = self.vk_session.method('users.get', {'user_id': user.vk_id})[0]['first_name']
								lname = self.vk_session.method('users.get', {'user_id': user.vk_id})[0]['last_name']
								user.nickname = nick
								user.save()
								print(nick)
								self.vk_session.method('messages.send', {
									'chat_id': msg['peer_id'] - 2000000000,
									'message': f'✅ Новый ник @id{user.vk_id}({uname} {lname}) - {user.nickname}',
									'random_id': 0
									})
					if text[0:11] == '/checkstats':
						search = text[12:]
						idf	 = re.findall(r'\[id(\d*)\|@.*]', search)[0]
						userf = utils.get_user_by_id(idf)
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):
									srokk = 'N/A'
									nsrok = 'N/A'

									if userf.adminstatus == 'Главный Администратор':
										userf.lvladmin = 7
										userf.save()
									if userf.adminstatus == 'Заместитель Главного Администратора':
										userf.lvladmin = 6
										userf.save()
									if userf.adminstatus == 'Куратор сервера':
										userf.lvladmin = 5
										userf.save()
									if userf.adminstatus == 'Главный Следящий':
										userf.lvladmin = 4
										userf.save()
									if userf.adminstatus == 'Администратор | Разработчик' or userf.adminstatus == 'Следящий':
										userf.lvladmin = 3
										userf.save()
									if userf.adminstatus == 'Разработчик':
										userf.lvladmin = 2
										userf.save()
									print(values_list)
									leaders_info = ''
									admin = 0
									for i in range(len(values_list)):
										if values_list[i] == userf.nickname:
											admin = 1
											val_list = worksheet.row_values(i + 1)
											print(val_list)
											userf.data = worksheet.get(f'E{i + 1}')[0][0]
											print(userf.data)
											if (i + 1) <= 7:
												rang = '[10]'
											else:
												rang = '[9]'
											userf.org = worksheet.get(f'A{i + 1}')[0][0]
											userf.discord = worksheet.get(f'B{i + 1}')[0][0]
											srokkfi = worksheet.get(f'F{i + 1}')[0][0]
											nsrok = worksheet.get(f'G{i + 1}')[0][0]
											if srokkfi == 'Отстоял':
												srokk = 'Отстоял свой срок ✅'
											else: srokk = f'{srokkfi} дней' # l = 11
											if (i + 1) <= 7:
												fraction = worksheet.get(f'A{i + 1}')[0][0]
												frac_list = worksheet.get(f'L5:O5')[0]
												print(frac_list)
												for i in range(len(frac_list)):
													if frac_list[i] == fraction:
														frac_viglist = worksheet.col_values(i + 12)
														print(frac_viglist)
														userf.pred = frac_viglist[6]
														print('pred =', userf.pred)
														nesnim = frac_viglist[7]
														userf.vigs = frac_viglist[5]
														userf.lgoti = frac_viglist[12]
														userf.save()
														leaders_info = f'\n⚠ Устные выговоры: {userf.pred}/3\n🚫 Выговоры: {userf.vigs}/5 ({nesnim} неснимаемых)\n💰 Льготы: {userf.lgoti}'

									uname = self.vk_session.method('users.get', {'user_id': userf.vk_id})[0]['first_name']
									lname = self.vk_session.method('users.get', {'user_id': userf.vk_id})[0]['last_name']

									if admin == 1:
										self.vk_session.method('messages.send', {
											'chat_id': msg['peer_id'] - 2000000000,
											'message': f'👥 Статистика {userf.nickname}\n\n🕵‍♂ Статус: {userf.adminstatus}\n🛡 Организация: {userf.org} {rang}{leaders_info}\n🔊 Discord: {userf.discord}\n🕓 Дата назначения: {userf.data}\n⌚ До срока: {srokk} \n💾 На посту: {nsrok} дней',
											'random_id': 0
											})
									if admin == 0:
										self.vk_session.method('messages.send', {
											'chat_id': msg['peer_id'] - 2000000000,
											'message': f'👥 Статистика {userf.nickname}\n\n🕵‍♂ Статус: {userf.adminstatus}',
											'random_id': 0
											})

					if text == '/mystats':
								srokk = 'N/A'
								nsrok = 'N/A'
								vigi = ''
								userf = utils.get_user_by_id(user_id)
								if userf.adminstatus == 'Главный Администратор':
										userf.lvladmin = 7
										userf.save()
								if userf.adminstatus == 'Заместитель Главного Администратора':
										userf.lvladmin = 6
										userf.save()
								if userf.adminstatus == 'Куратор сервера':
										userf.lvladmin = 5
										userf.save()
								if userf.adminstatus == 'Главный Следящий':
										userf.lvladmin = 4
										userf.save()
								if userf.adminstatus == 'Администратор | Разработчик' or userf.adminstatus == 'Следящий':
										userf.lvladmin = 3
										userf.save()
								if userf.adminstatus == 'Разработчик':
										userf.lvladmin = 2
										userf.save()
								print(values_list)
								admin = 1
								for i in range(len(values_list)):
									if values_list[i] == userf.nickname:
										admin = 0
										val_list = worksheet.row_values(i + 1)
										print(val_list)
										userf.data = worksheet.get(f'E{i + 1}')[0][0]
										print(userf.data)
										userf.discord = worksheet.get(f'B{i + 1}')[0][0]
										srokkfi = worksheet.get(f'F{i + 1}')[0][0]
										nsrok = worksheet.get(f'G{i + 1}')[0][0]
										if (i + 1) <= 7:
												rang = '[10]'
										else:
												rang = '[9]'
										userf.org = worksheet.get(f'A{i + 1}')[0][0]
										if srokkfi == 'Отстоял':
											srokk = 'Отстоял свой срок'
										else: srokk = f'{srokkfi} дней' # l = 11
										if (i + 1) <= 7:
											fraction = worksheet.get(f'A{i + 1}')[0][0]
											frac_list = worksheet.get(f'L5:O5')[0]
											print(frac_list)
											for i in range(len(frac_list)):
												if frac_list[i] == fraction:
													frac_viglist = worksheet.col_values(i + 12)
													print(frac_viglist)
													userf.pred = frac_viglist[6]
													print('pred =', userf.pred)
													nesnim = frac_viglist[7]
													userf.vigs = frac_viglist[5]
													userf.lgoti = frac_viglist[12]
													userf.save()
													vigi = f'\n⚠ Устные выговоры: {userf.pred}/3\n🚫 Выговоры: {userf.vigs}/5 ({nesnim} неснимаемых)\n💰 Льготы: {userf.lgoti}'
								uname = self.vk_session.method('users.get', {'user_id': userf.vk_id})[0]['first_name']
								lname = self.vk_session.method('users.get', {'user_id': userf.vk_id})[0]['last_name']
								if admin == 0:
									self.vk_session.method('messages.send', {
										'chat_id': msg['peer_id'] - 2000000000,
										'message': f'👥 Статистика {userf.nickname}\n\n🕵‍♂ Статус: {userf.adminstatus}\n🛡 Организация: {userf.org} {rang}{vigi}\n🔊 Discord: {userf.discord}\n🕓 Дата назначения: {userf.data}\n⌚ До срока: {srokk} \n💾 На посту: {nsrok} дней',
										'random_id': 0
										})
								if admin == 1:
									self.vk_session.method('messages.send', {
										'chat_id': msg['peer_id'] - 2000000000,
										'message': f'👥 Статистика {userf.nickname}\n\n🕵‍♂ Статус: {userf.adminstatus}',
										'random_id': 0
										})
					if text[0:5] == '/kick':
						search = text[6:]
						idf, reason = re.findall(r'\[id(\d*)\|@.*] (.*)', search)[0]
						userf = utils.get_user_by_id(idf)
						texts = ''
						org = ''
						if int(user.lvladmin) >= 2:
							if int(user.lvladmin) >= int(userf.lvladmin):
								try:
									for i in range(len(values_list)):
										if values_list[i] == userf.nickname:
											val_list = worksheet.row_values(i + 1)

											print(val_list)
											org = val_list[0]
											discordid = val_list[1]
											vk = userf.vk_id
											nick = val_list[3]
											data = val_list[4]
											dosroka = val_list[5]
											napostu = val_list[6]
											otpusk = val_list[7]
											print(i)
											worksheet.update(f'B{i + 1}', '')
											worksheet.update(f'C{i + 1}', 'VK')
											worksheet.update(f'E{i + 1}', '')
											worksheet.update(f'D{i + 1}', '')
											fraction = worksheet.get(f'A{i + 1}')[0][0]
											frac_list = worksheet.get(f'L5:O5')[0]
											print(frac_list)
											if i + 1 <= 7:
												for i in range(len(frac_list)):
													if frac_list[i] == fraction:
														frac_viglist = worksheet.col_values(i + 12)
														print(frac_viglist)
														ust = frac_viglist[6]
														print('pred =', userf.pred)
														nesnim = frac_viglist[7]
														strogie = frac_viglist[5]
														lgoti = frac_viglist[12]
														userf.save()
														vigi = f'\nУстные выговоры: {userf.pred}\nВыговоры: {userf.vigs}/5 ({nesnim} неснимаемых)\nЛьготы: {userf.lgoti}'
														otkaz = val_list[8]
														zvanie = val_list[9]
														texts = f'\nОтказов за срок: {otkaz}\nЗвание: {zvanie}\nЛьготы: {lgoti}\nСтрогие выговоры: {strogie} ({nesnim} неснимаемых)\nУстные выговоры: {ust}\n'
														valcol = logsheet.col_values(2)
														a = len(valcol) + 1
														user = utils.get_user_by_id(user_id)
														if ust != 0:
															logsheet.update(f'B{a}', int(ust))
															logsheet.update(f'C{a}', 'Устный')
															logsheet.update(f'D{a}', 'Нет')
															logsheet.update(f'E{a}', reason)
															logsheet.update(f'F{a}', user.nickname)
															logsheet.update(f'G{a}', worksheet.get('K2'))
															logsheet.update(f'A{a}', fraction)
														a = len(valcol) + 1
														user = utils.get_user_by_id(user_id)
														if strogie != 0:
															logsheet.update(f'B{a}', int(strogie))
															logsheet.update(f'C{a}', 'Строгий')
															logsheet.update(f'D{a}', 'Нет')
															logsheet.update(f'E{a}', reason)
															logsheet.update(f'F{a}', user.nickname)
															logsheet.update(f'G{a}', worksheet.get('K2'))
															logsheet.update(f'A{a}', fraction)
														valcol = lgotsheet.col_values(2)
														a = len(valcol) + 1
														if lgoti != 0:
															lgotsheet.update(f'B{a}', int(lgoti))
															lgotsheet.update(f'C{a}', 'Нет')
															lgotsheet.update(f'D{a}', reason)
															lgotsheet.update(f'E{a}', user.nickname)
															lgotsheet.update(f'F{a}', worksheet.get('K2'))
															lgotsheet.update(f'A{a}', fraction)

									i = 0

									search = text[6:]
									idf, reason = re.findall(r'\[id(\d*)\|@.*] (.*)', search)[0]
									self.vk_session.method('messages.send', {
    									'chat_id': 1,
    									'message': f'✅[{user.adminstatus} ({user.lvladmin} lvl)] {user.nickname} кикнул {userf.nickname}({userf.org}) с причиной: {reason}.\n\nДанные из таблицы:\nОрганизация: {org}\nDiscord ID: {discordid}\nVK ID: @id{vk}\nДата назначения: {data}\nДо срока: {dosroka}\nДней на посту: {napostu}\nОтпусков за срок: {otpusk}{texts}\n\n Внимание! Если данные из таблицы взяты неверно, сообщите @id394757065(разработчику) бота или Администратору Vladimir_Romanov',
    									'random_id': 0
                					})
									print(idf, reason)
									kickuser = utils.get_user_by_id(idf)
									print('до цикла while дошел')
									while i != len(chat_ids):
											print('кол-во элементов', len(chat_ids))
											print('цикл while начался')
											try:
												self.vk_session.method('messages.removeChatUser', {
													'user_id': kickuser.vk_id,
													'chat_id': chat_ids[i]
													})
												print('кикнул')
												self.vk_session.method('messages.send', {
													'chat_id': chat_ids[i],
													'message': f'✅@id{kickuser.vk_id} ({kickuser.nickname}) [{kickuser.org}] был кикнут со всех бесед по запросу: @id{user.vk_id} ({user.nickname}) по причине: {reason}',
													'random_id': 0
													})
												i += 1
												print('i в TRY:', i)
											except:
												i += 1
												print('i в EXCEPT:', i)
								except vk_api.exceptions.ApiError as e:
									print(e)
							else:
								self.vk_session.method('messages.send', {
								'chat_id': msg['peer_id'] - 2000000000,
								'message': f'❌Нельзя выполнить какие-либо действия с пользователем, выше Вас статусом.',
								'random_id': 0
								})



					return VkBot().run()
				except vk_api.exceptions.ApiError as e:
					if e.code != 935:
									errormsg = e.error['error_msg']
									self.vk_session.method('messages.send', {
												'chat_id': msg['peer_id'] - 2000000000,
												'message': f'❌ Произошла ошибка, возможно ID пользователя не найден или он не существует в беседе.(\n\nКод ошибки:\n [{e.code}] {errormsg}',
												'random_id': 0
									})

					return VkBot().run()
				except IndexError:
					self.vk_session.method('messages.send', {
												'chat_id': msg['peer_id'] - 2000000000,
												'message': f'❌ Ошибка! Вы не ввели какое-то значение!\n Код ошибки: {IndexError}',
												'random_id': 0
									})
					return VkBot().run()
				finally:
					self.vk_session.method('messages.send', {
											'chat_id': msg['peer_id'] - 2000000000,
											'message': f'❌ Что-то пошло не так. Повторите попытку. Код ошибки: неизвестно.',
											'random_id': 0
									})
					return VkBot().run()








if __name__ == '__main__':
    VkBot().run()