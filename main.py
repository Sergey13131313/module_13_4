from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message

from Config import API_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.message import Message

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

data = None
COUNT = 0


def calcCalorie(age=0, growth=0, weight=0):
    return ((10 * weight) + (6.25 * growth) + (5 * age) + 5)


class UserParamState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['Кузя'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(lambda message: message.text.lower() == 'calories')
async def userRegistr(message):
    await message.answer('Введите свой возраст')
    await UserParamState.age.set()


@dp.message_handler(state=UserParamState.age)
async def setAge(message, state):
    global COUNT
    if not message.text.isdigit() and COUNT < 3:
        await message.answer('Эх, не правлиьно!\nПопробуй ещё раз')
        COUNT += 1
        print(COUNT)
    elif not message.text.isdigit() and COUNT == 3:
        await message.answer('Ну и не считаем значит каллории')
        COUNT = 0
        await state.finish()
    else:
        COUNT = 0
        await state.update_data(age_state=message.text)
        await message.answer(f'Ввведите свой рост')
        await UserParamState.growth.set()


@dp.message_handler(state=UserParamState.growth)
async def setGrowth(message, state):
    global COUNT
    if not message.text.isdigit() and COUNT < 3:
        await message.answer('Эх, не правлиьно!\nПопробуй ещё раз')
        COUNT += 1
        print(COUNT)
    elif not message.text.isdigit() and COUNT == 3:
        await message.answer('Ну и не считаем значит каллории')
        COUNT = 0
        await state.finish()
    else:
        await state.update_data(growth_state=message.text)
        await message.answer(f'Ввведите свой вес')
        await UserParamState.weight.set()


@dp.message_handler(state=UserParamState.weight)
async def setWeight(message, state):
    global data
    global COUNT
    if not message.text.isdigit() and COUNT < 3:
        await message.answer('Эх, не правлиьно!\nПопробуй ещё раз')
        COUNT += 1
        print(COUNT)
    elif not message.text.isdigit() and COUNT == 3:
        await message.answer('Ну и не считаем значит каллории')
        COUNT = 0
        await state.finish()
    else:
        await state.update_data(weight_data=message.text)
        data = await state.get_data()
        await state.finish()
        for key, value in data.items():
            print(key, value)
        a = data['age_state']
        cal = calcCalorie(age=int(data['age_state']), growth=int(data['growth_state']), weight=int(data['weight_data']))
        await message.answer(f'Суточное потребление калорий {cal}')


@dp.message_handler()
async def all_massages(message):
    await message.answer('Я Кузя, привет!')


executor.start_polling(dp, skip_updates=True)
