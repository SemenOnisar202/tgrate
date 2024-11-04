import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7164140072:AAHdmvzomy6_s8j6lERwjpVHZuGTRVtkkNI'
API_KEY = '88d7ea01-9837-4bd0-80e9-ead7e2e04eb3'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
file = open('hNZ3NP6qtL8.jpg','rb')
message_ids = {}

def get_currency_rates(symbol):
    headers = {
        'Accept': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert': 'USD',
    }

    response = requests.get(url, headers=headers, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        return None


async def send_currency_rate(symbol, currency_name, message):
    rates = get_currency_rates(symbol)
    if rates and 'data' in rates and symbol in rates['data']:
        price = rates['data'][symbol]['quote']['USD']['price']
        reply = f'Курс {currency_name}: ${price:.2f} USD'
    else:
        reply = 'Не удалось получить данные о курсе. Попробуйте позже.'

    if message_ids.get(currency_name):
        await bot.delete_message(chat_id=message.chat.id, message_id=message_ids[currency_name])

    new_message = await message.answer(reply)
    message_ids[currency_name] = new_message.message_id

@dp.callback_query_handler(lambda call: call.data in ['Rate','Ethereum_rate', 'Troncoin_rate', 'Toncoin_rate', 'Bitcoin_rate'])
async def callback_query(call: types.CallbackQuery):
    if call.data == 'Rate':
        await menu_command(call.message)
    if call.data == 'Ethereum_rate':
        await send_currency_rate('ETH', 'Ethereum', call.message)
    elif call.data == 'Troncoin_rate':
        await send_currency_rate('TRX', 'Troncoin', call.message)
    elif call.data == 'Toncoin_rate':
        await send_currency_rate('TON', 'Toncoin', call.message)
    elif call.data == 'Bitcoin_rate':
        await send_currency_rate('BTC', 'Bitcoin', call.message)





@dp.message_handler(commands=['курсы'.lower(),'rate'.lower(),'курсы'.lower()])
async def menu_command(message: types.Message):
    ratekb = InlineKeyboardMarkup()
    rateButton1 = InlineKeyboardButton(text='Курс Troncoin', callback_data='Troncoin_rate')
    rateButton2 = InlineKeyboardButton(text='Курс Ethereum', callback_data='Ethereum_rate')
    rateButton3 = InlineKeyboardButton(text='Курс Toncoin', callback_data='Toncoin_rate')
    rateButton4 = InlineKeyboardButton(text='Курс Bitcoin', callback_data='Bitcoin_rate')

    ratekb.add(rateButton1, rateButton2, rateButton3, rateButton4)

    if message_ids.get('menu'):
        await bot.delete_message(chat_id=message.chat.id, message_id=message_ids['menu'])

    new_message = await message.answer('📈Курсы: TRX, ETH, TRON, BTC', reply_markup=ratekb)
    message_ids['menu'] = new_message.message_id

@dp.callback_query_handler(lambda call: call.data in ['Rate'])
async def callback_query1(call: types.CallbackQuery):
    if call.data == 'Rate':
        await menu_command(call.message)


@dp.message_handler(commands=['start'.lower(),'старт'.lower()])
async def star(message: types.Message):
    await bot.send_photo(message.chat.id, file)
    ratekbz = InlineKeyboardMarkup()
    rate = InlineKeyboardButton(text='Посмотреть курсы', callback_data='Rate')
    ratekbz.add(rate)
    await bot.send_message(chat_id=message.chat.id, text='💵Привет! Я бот для получения курса таких альтов как: Troncoin, Ethereum, Toncoin, Bitcoin. Используй команду </rate>, </курс> для получения текущего курса.💵', reply_markup=ratekbz)

if __name__ == '__main__':
    executor.start_polling(dp)