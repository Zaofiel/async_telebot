import asyncio
import config
import telebot
from telebot.async_telebot import AsyncTeleBot

class Car:
    def __init__(self):
        self.color = 'Вы не выбрали цвет'
        self.brand = 'Вы не выбрали бренд'

    def set_color(self, color):
        self.color = color

    def set_brand(self, brand):
        self.brand = brand

bot = AsyncTeleBot(config.token)
cars = {}

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = """Привет,
создай машину с помощью команды /car"""
    await bot.reply_to(message, text)

@bot.message_handler(commands=['car'])
async def car(message):
    chat_id = message.chat.id
    cars[chat_id] = Car()
    await bot.send_message(chat_id, '''Вы создали машину,
взаимодействуйте с ней с помощью команд:
/info - информация о машине
/color - изменить цвет
/brand - изменить бренд''')

@bot.message_handler(commands=['color'])
async def color(message):
    chat_id = message.chat.id
    if chat_id not in cars:
        await bot.send_message(chat_id, 'Вы не создали машину')
        return

    args = telebot.util.extract_arguments(message.text)
    if args is None:
        await bot.send_message(chat_id, 'Вы не указали цвет')
    else:
        cars[chat_id].set_color(args)
        await bot.send_message(chat_id, f'Вы указали цвет: {args}')

@bot.message_handler(commands=['brand'])
async def brand(message):
    chat_id = message.chat.id
    if chat_id not in cars:
        await bot.send_message(chat_id, 'Вы не создали машину')
        return

    args = telebot.util.extract_arguments(message.text)
    if args is None:
        await bot.send_message(chat_id, 'Вы не указали бренд')
    else:
        cars[chat_id].set_brand(args)
        await bot.send_message(chat_id, f'Вы указали бренд: {args}')

@bot.message_handler(commands=['info'])
async def info(message):
    chat_id = message.chat.id
    if chat_id not in cars:
        await bot.send_message(chat_id, 'Вы не создали машину')
        return

    car = cars[chat_id]
    await bot.send_message(chat_id, f'''Цвет: {car.color}
Бренд: {car.brand}''')

asyncio.run(bot.polling())