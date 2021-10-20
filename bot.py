#импортируем нужные компоненты
from glob import glob
import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from random import choice, randint

import settings

#добавляем базовое логирование
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#добавляем функцию с reply-клавиатурой с основными управляющими кнопками
def main_keyboard():
	#создаем переменную, содержащую reply-клавиатуру с кнопками, которая будет выводится всегда
	replykeyboard= [[
		KeyboardButton("КАТЕГОРИИ"),
		KeyboardButton("СТОП-ИГРА")
		]]
	#назначаем переменную в которой содержится клавиатура полностью
	my_keyboard = ReplyKeyboardMarkup(replykeyboard, resize_keyboard = True)
	#назначаем вывод клавиатуры на экран
	return my_keyboard

#добавляем функцию с inline-клавиатурой с наваниями категорий, в которых будут выдаваться катрочки
def get_inline():
	#создаем переменную-массив inline-кнопок с callback, где каждому словарю(категории) соответствует кнопка с назанием
	inlinekeyboard= [
		#создаем отдельную кнопку для каждой категории внутри массива
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
	#назначаем переменную в которой содержится клавиатура полностью
	my_inline_keyboard = InlineKeyboardMarkup(inlinekeyboard)
	#вывод клавиатуры на экран
	return my_inline_keyboard

#создаем функцию, которая будет приветствовать пользователя при нажатии конпки start
def greet_user(update, context):
	#собираем информацию "имя пользователя" и сохраняем в переменную для последующего вывода
	name = update.message.chat.first_name
	#создаем переменные с приветственным текстом и подсказками для последующего вывода
	txt_greet = "Привет, {}! Данный бот поможет, если под рукой нет ручки и бумаги. Просто следуй подсказкам бота, выбирай тематику и начинай играть.".format(name)
	txt_prompt1 = "Чтобы играть было удобнее, отключи в настройках телефона автоблокировку экрана и режим энергосбережения на время игры."
	txt_prompt2 = "Отключи блокировку книжной ориентации."
	txt_choice = "Чтобы продолжить игру нажми кнопку КАТЕГОРИИ. Если хочешь остановить бота нажми кнопку СТОП-ИГРА."
	#вывод приветственного сообщения на экран
	update.message.reply_text(txt_greet)
	#вывод сообщений-подсказок на экран
	update.message.reply_text(txt_prompt1)
	update.message.reply_text(txt_prompt2)
	#вывод сообщения-рычага и основоной клавиатуры на экран
	update.message.reply_text(txt_choice, reply_markup = main_keyboard())

#создаем функцию выбора категорий, которая проинструктирует юзера о дальнейших действиях и выдаст клавиатуру с категориями
def categories(update, context):
	#создаем переменные с подсказками для последующего вывода
	txt_choice1 = "Все игроки в комнате выбирают одинаковую категорию."
	txt_choice2 = "Выбери одну из категорий и наслаждайся игрой."
	txt_prompt3 = "Нажав на кнопку, ты получишь случайную карточку из выбранной категории."
	txt_prompt4 = "Щелкни по карточке, раскрыв ее на весь экран. Переверни телефон в горизонтальное положение, экраном от себя так, чтобы не видеть карточку. У тебя на это будет 5 секунд после получения карточки."
	#вывод сообщений-подсказок на экран
	update.message.reply_text(txt_choice1)
	#вывод сообщения-рычага и инлайн-клавиатуры на экран
	update.message.reply_text(txt_choice2, reply_markup = get_inline())
	update.message.reply_text(txt_prompt3)
	update.message.reply_text(txt_prompt4)

#добавим функцию, которая анализирует callback с кнопки, нажатой пользователем, и выводит карточку соответсвующей категории
def send_card(update, context):
	#назначаем переменную и собираем в нее данные callback с кнопок клавиатуры
	query_data = update.callback_query.data
	#добавляем условный оператор, чтобы задать направление движения программы в соответствии с выбранной юзером категорией
	if query_data == "city":
		#назначаем переменную с path, по которому будет осуществляться поиск карточки(для каждой категории)
		cards_list = glob('cards/cities/*.gif');
	elif query_data == "animal":
		cards_list = glob('cards/animals/*.gif');
	elif query_data == "houseware":
		cards_list = glob('cards/houseware/*.gif');
	elif query_data == "actors":
		cards_list = glob('cards/actors/*.gif');
	elif query_data == "food":
		cards_list = glob('cards/food/*.gif');
	elif query_data == "politicians":
		cards_list = glob('cards/politicians/*.gif');
	elif query_data == "superheroes":
		cards_list = glob('cards/superheroes/*.gif');
	elif query_data == "plants":
		cards_list = glob('cards/plants/*.gif');
	elif query_data == "sightseeings":
		cards_list = glob('cards/sightseeings/*.gif');
	else:
		cards_list = glob('cards/profession/*.gif')
	#назначаем переменную с id чата из данных, полученных от пользователя, она нам понадобится для отправки карточки
	chat_id = update.effective_chat.id
	#назначаем переменную с рандомным выбором карточки из соответствующей папки
	cardname = choice(cards_list)
	#отправляем выбранную рандомно ранее карточку пользователю
	context.bot.send_animation(chat_id=chat_id, animation=open(cardname, "rb"))

#создаем функцию принудительной остановки бота
def stop_game(update, context):
	#вывод на экран сообщения с прощальным текстом
	update.message.reply_text("Жаль, что уже уходишь! Заглядывай еще!")
	#операция принудительной остановки бота
	updater.stop()

def main():
	#создаем бота и передаем ему ключ для авторизации на серверах Telegram
  mybot = Updater(settings.API_KEY, use_context=True)
  #добавляем диспетчер, который будет реагировать на событие
  dp = mybot.dispatcher
  #добавляем хендлеры для обработки событий
  dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
  dp.add_handler(CallbackQueryHandler(send_card, pass_user_data=True))
  dp.add_handler(MessageHandler(Filters.regex('^(СТОП-ИГРА)$'), stop_game, pass_user_data=True))
  dp.add_handler(MessageHandler(Filters.regex('^(КАТЕГОРИИ)$'), categories, pass_user_data=True))
  #командуем боту начать ходить в Telegram за сообщениями
  mybot.start_polling()
  #запускаем бота, он будет работать, пока мы его не остановим принудительно
  mybot.idle()


if __name__ == "__main__":
	main()
