from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

# Функция для старта бота
@router.message(Command(commands=['start']))
async def cmd_start(message:Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text = "Привет! Этот бот может поворачивать матрицу на 90 градусов.\nВведите матрицу.", 
        reply_markup=ReplyKeyboardRemove()
    )

# Функция для сброса состояния бота
@router.message(Command(commands=['reset']))
async def cmd_reset(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text = "Состояние сброшено. Введите новую матрицу.", 
        reply_markup=ReplyKeyboardRemove()
    )