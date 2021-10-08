# Импортируем нужные компоненты
from glob import glob
import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from random import choice, randint

import settings

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main_keyboard():
	#Создаем переменную с реплай клавиатурой
	replykeyboard= [[
		KeyboardButton("КАТЕГОРИИ"),
		KeyboardButton("СТОП-ИГРА")
		]]
	my_keyboard = ReplyKeyboardMarkup(replykeyboard, resize_keyboard = True)
	return my_keyboard

def get_inline():
	inlinekeyboard= [
		[InlineKeyboardButton('ГОРОДА', callback_data = "city")],
		[InlineKeyboardButton('ЖИВОТНЫЕ', callback_data = "animal")],
		[InlineKeyboardButton('ПРЕДМЕТЫ БЫТА', callback_data = "houseware")],
		[InlineKeyboardButton('АКТЕРЫ', callback_data = "actors")],
		[InlineKeyboardButton('ПРОФЕССИИ', callback_data = "profession")],
		[InlineKeyboardButton('ЕДА', callback_data = "food")],
		[InlineKeyboardButton('ПОЛИТИКИ', callback_data = "politicians")],
		[InlineKeyboardButton('СУПЕРГЕРОИ', callback_data = "superheroes")],
		[InlineKeyboardButton('РАСТЕНИЯ', callback_data = "plants")],
		[InlineKeyboardButton('ДОСТОПРИМЕЧАТЕЛЬНОСТИ', callback_data = "sightseeings")]
		]
	my_inline_keyboard = InlineKeyboardMarkup(inlinekeyboard)
	return my_inline_keyboard

#Создаем функцию, которая будет приветствовать пользователя при нажатии конпки start
def greet_user(update, context):
	#В терминал будет выводится инфо о пользователе
	print(update.message)
	#Собираем информацию "имя пользователя" и сохраняем в переменную для последующего вывода
	name = update.message.chat.first_name
	#Создаем переменную с приветственным текстом для последующего вывода
	text = "Привет, {}! Данный бот поможет, если нет ручки и бумаги. Просто следуй подсказкам бота, выбирай тематику и начинай играть. Если хочешь продолжить игру нажми кнопку КАТЕГОРИИ. Чтобы отсановить бота нажми СТОП-ИГРА".format(name)
	#На экране выводится приветственное сообщение
	update.message.reply_text(text, reply_markup = main_keyboard())

def stop_game(update, context):
	update.message.reply_text("Жаль, что уже уходишь! Приходи исчо!")
	#updater.stop()

def categories(update, context):
	txt_choice = "Выберите одну из приведенных ниже категорий. Все игроки в комнате выбирают одинаковую категорию."
	update.message.reply_text(txt_choice, reply_markup = get_inline())


def send_card(update, context):
	query = update.callback_query
	query_data = update.callback_query.data
	if query_data == "city":
		cards_list = glob('cards/cities/*.png');
	elif query_data == "animal":
		cards_list = glob('cards/animals/*.png');
	elif query_data == "houseware":
		cards_list = glob('cards/houseware/*.png');
	elif query_data == "actors":
		plug = glob('cards/actors/1/*.png')
		cards_list = glob('cards/actors/*.png');
	elif query_data == "food":
		cards_list = glob('cards/food/*.png');
	elif query_data == "politicians":
		cards_list = glob('cards/politicians/*.png');
	elif query_data == "superheroes":
		cards_list = glob('cards/superheroes/*.png');
	elif query_data == "plants":
		cards_list = glob('cards/plants/*.png');
	elif query_data == "sightseeings":
		cards_list = glob('cards/sightseeings/*.png');
	else:
		cards_list = glob('cards/profession/*.png')
	plug1 = choice(glob('cards/actors/1/*.png'))
	cardname = choice(cards_list)
	chat_id = update.effective_chat.id
	query.edit_message_text("Отключите блокировку книжной ориентации на телефоне, переверните телефон в горизонтальное положение экраном от себя, а также увеличьте время до перехода телефона в спящий режим или вовсе отключите спящй режим на время игры")
	context.bot.send_photo(chat_id=chat_id, photo=open(plug1, "rb"))
	context.bot.edit_message_media(chat_id=chat_id, message_id = plug1, media = cardname)



def main():
	# Создаем бота и передаем ему ключ для авторизации на серверах Telegram
  mybot = Updater(settings.API_KEY, use_context=True)
  #Добавляем диспетчер, который будет реагировать на стратовое событие
  dp = mybot.dispatcher
  dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
  dp.add_handler(CallbackQueryHandler(send_card))
  dp.add_handler(MessageHandler(Filters.regex('^(СТОП-ИГРА)$'), stop_game, pass_user_data=True))
  dp.add_handler(MessageHandler(Filters.regex('^(КАТЕГОРИИ)$'), categories, pass_user_data=True))
  # Командуем боту начать ходить в Telegram за сообщениями
  logging.info("Бот стартовал")
  mybot.start_polling()
  # Запускаем бота, он будет работать, пока мы его не остановим принудительно
  mybot.idle()


if __name__ == "__main__":
	main()
