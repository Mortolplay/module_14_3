from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.add(button_1)
kb.add(button_2)

ikb = InlineKeyboardMarkup()
i_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
i_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

catalog_kb = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
catalog_kb.insert(button1)
catalog_kb.insert(button2)
catalog_kb.insert(button3)
catalog_kb.insert(button4)

buy_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button22 = KeyboardButton(text='Информация')
button33 = KeyboardButton(text='Купить')
buy_kb.insert(button)
buy_kb.insert(button22)
buy_kb.insert(button33)

@dp.message_handler(text = "о нас")
async def price(message):
    with open('filtes/1.png', "rb") as img:
        await message.answer_photo(img, f'Название: Product1 | Описание: описание <number> | Цена: 100')
    with open('filtes/2.png', "rb") as img:
        await message.answer_photo(img, f'Название: Product2 | Описание: описание <number> | Цена: 200')
    with open('filtes/3.png', "rb") as img:
        await message.answer_photo(img, f'Название: Product3 | Описание: описание <number> | Цена: 300')
    with open('filtes/4.png', "rb") as img:
        await message.answer_photo(img, f'Название: Product4 | Описание: описание <number> | Цена: 400')
    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.message_handler(text='Привет')
async def start(message):
    await message.answer(f'Привет! Я бот помогающий Вашему здоровью.\n'
                         f'Чтобы начать, нажмите "Рассчитать"', reply_markup=kb)

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories_m = 10 * weight + 6.25 * growth - 5 * age + 5
    calories_w = 10 * weight + 6.25 * growth - 5 * age - 161

    global a
    global g
    global w
    global c_m
    global c_w
    a = age
    g = growth
    w = weight
    c_m = calories_m
    c_w = calories_w
    await message.answer('Расчёт произведён, посмотрите информацию')

    @dp.message_handler(text='Информация')
    async def inform(message):
        await message.answer(f'Ваш возраст:  {a}\nВаш рост:      {g}\nВаш вес:          {w}\n'
                             f'Ваша норма калорий: {c_m}, если вы мужчина\n    '
                             f'                                      {c_w}, если вы женщина')

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
