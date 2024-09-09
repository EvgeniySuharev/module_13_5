import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token='')
dp = Dispatcher()
router = Router()

kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'),
                                    KeyboardButton(text='Информация')]], resize_keyboard=True)


class UsesState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@router.message(CommandStart())
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@router.message(F.text == 'Информация')
async def info(message):
    await message.answer('Информация:\nЭто учебный бот университета Urban. Он помогает твоему'
                         'здоровью!')


@router.message(F.text == 'Рассчитать')
async def set_age(message, state: FSMContext):
    await state.set_state(UsesState.age)
    await message.answer('Введите свой возраст:')


@router.message(UsesState.age)
async def set_growth(message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(UsesState.growth)
    await message.answer('Введите свой рост:')


@router.message(UsesState.growth)
async def set_weight(message, state: FSMContext):
    await state.update_data(growth=message.text)
    await state.set_state(UsesState.weight)
    await message.answer('Введите свой вес:')


@router.message(UsesState.weight)
async def send_calories(message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    a = int(data['age'])
    g = int(data['growth'])
    w = int(data['weight'])
    res = 10 * w + 6.25 * g - 5 * a + 5
    await message.answer(f'Ваша норма: {res} ккал/сутки')
    await state.clear()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
