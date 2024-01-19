from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import numpy as np



router = Router()

available_commands = ["/clockwise", "/counterclockwise"]

# Регестрируем состояния
class MatrixForm(StatesGroup):
    WaitingForMatrix = State()
    WaitingForDirection = State()

# Первое состояние ждет ввода данных от пользователя
@router.message(StateFilter(None))
async def process_matrix(message: Message, state: FSMContext,):
    try:
        matrix = np.array([list(map(int, row.split())) for row in message.text.split('\n')])
        if matrix.size == 0:
            raise ValueError("Input matrix is empty.")
        await state.update_data(matrix_data={"matrix": matrix})
        await message.answer("Матрица успешно принята.")
        await message.answer(str(matrix))
        await state.set_state(MatrixForm.WaitingForDirection)
    except ValueError as e:
        await message.answer(f"Ошибка: {str(e)}")
        return

# Второе состояние преобразует данные
@router.message(MatrixForm.WaitingForDirection)
async def process_direction(message: Message, state: FSMContext):
    await state.update_data(direction=message.text.lower())
    await message.answer('Выберите направление поворота: /clockwise или /counterclockwise')
    if message.text.lower() in ['/clockwise', '/counterclockwise']:
        direction = message.text.lower()
        matrix_data = await state.get_data()
        matrix = matrix_data.get('matrix')
        print("Matrix Data:", matrix_data)  # Add this line to check the matrix_data
        print("Matrix:", matrix)  # Add this line to check the matrix
        
        rotated_matrix = rotate_matrix(matrix, direction)
        await message.answer(f"Повернутая матрица:\n{rotated_matrix}")
        await state.clear()
        await state.set_state(MatrixForm.WaitingForMatrix)
    else:
        await message.answer("Выберите направление поворота: /clockwise или /counterclockwise")

# Функция для поворота матрицы
def rotate_matrix(matrix, direction):
    if matrix.size == 0:
        return matrix  # Return the same empty matrix
    if direction == '/clockwise':
        return np.rot90(matrix, -1)
    elif direction == '/counterclockwise':
        return np.rot90(matrix, 1)
    else:
        return matrix
