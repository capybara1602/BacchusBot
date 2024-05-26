from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from Keyboard.pagination_kb import create_pagination_keyboard, create_inline_kb
from lexicon.lexicon import LEXICON
from services.file_handling import book
from SQL_files.wine_selection import bd_wine, execute_read_query, create_conection, output_wine


router = Router()

storage = MemoryStorage()

data_to_wine = {}



    

class FSMFillForm(StatesGroup):
    fill_food = State()
    fill_price_from = State()
    fill_price_to = State()

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    keyboard = create_inline_kb(1,'history', 'production', 'questions')
    text = LEXICON['/start']
    await message.answer(
        text=text,
        reply_markup=keyboard
    )
    


#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Главное меню"
@router.callback_query(F.data == 'menu')
async def process_menu_press(callback: CallbackQuery):
    keyboard = create_inline_kb(1,'history', 'production', 'questions')
    await callback.message.edit_text(
        text = 'Выбери интересующую категорию',
        reply_markup=keyboard
    )


#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "История появления вина"
@router.callback_query(F.data == 'history')
async def process_history_press(callback: CallbackQuery):
    text = book[LEXICON['history']]
    await callback.message.edit_text(
        text = text,
        reply_markup=create_pagination_keyboard('menu')
    )
 

#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Процесс производства вина"
@router.callback_query(F.data == 'production')
async def process_production_press(callback: CallbackQuery):
    keyboard = create_inline_kb(3,'white wine', 'red wine', 'rose wine', 'sparkling wine',
                                 'fortified wine', 'menu')
    text = book['Виды вина']
    await callback.message.edit_text(
        text = text,
        reply_markup=keyboard
    )

#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Белое вино"
@router.callback_query(F.data == 'white wine')
async def process_white_wine_press(callback: CallbackQuery):
    text = book[LEXICON['white wine']]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'production'
            )
    )

#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Красное вино"
@router.callback_query(F.data == 'red wine')
async def process_red_wine_press(callback: CallbackQuery):
    text = book[LEXICON['red wine']]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'production'
        )
    )

#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Розовое вино"
@router.callback_query(F.data == 'rose wine')
async def process_rose_wine_press(callback: CallbackQuery):
    text = book[LEXICON['rose wine']]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'production'
        )
    )

#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Игристое вино"
@router.callback_query(F.data == 'sparkling wine')
async def process_sparkling_wine_press(callback: CallbackQuery):
    text = book[LEXICON['sparkling wine']]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'production'
        )
    )

#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Крепленое вино"
@router.callback_query(F.data == 'fortified wine')
async def process_fortified_wine_press(callback: CallbackQuery):
    text = book[LEXICON['fortified wine']]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'production'
        )
    )



#Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Помощь в выборе вина"
@router.callback_query(StateFilter(default_state), F.data == 'questions')
async def process_questions_command(callback: CallbackQuery, state: FSMContext):
    markup = create_inline_kb(2, 'Говядина', 'Рыба', 'Выдержанный сыр', 'Морепродукты', 'Утка', 'Сыр', 'Закуски, салаты и антипасто', 'Курица', 'Свинина', 'Ягненок', 'Паста', 'Мягкий сыр', 'Овощи',
                               'Азиатская кухня', 'Десерты и выпечка', 'Кролик', 'Оленина', 'Ризотто', 'Грибы', 'Фрукты и ягоды', 'Хамон', 'Салями', 'Японская кухня', 'Шоколад', 'Бургер')
    text = LEXICON['Помощь в выборе вина']
    await callback.message.edit_text(
        text = text,
        reply_markup=markup
    )
    await state.set_state(FSMFillForm.fill_food)


@router.callback_query(StateFilter(FSMFillForm.fill_food), F.data.in_(['Говядина', 'Рыба', 'Выдержанный сыр', 'Морепродукты', 'Утка', 'Сыр', 'Закуски, салаты и антипасто', 'Курица', 'Свинина',
                                                                        'Ягненок', 'Паста', 'Мягкий сыр', 'Овощи', 'Азиатская кухня', 'Десерты и выпечка', 'Кролик', 'Оленина', 'Ризотто', 'Грибы',
                                                                        'Фрукты и ягоды', 'Хамон', 'Салями', 'Японская кухня', 'Шоколад', 'Бургер']))
async def process_questions_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(food=callback.data)
    await callback.message.delete()

    await callback.message.answer(
        text='Укажите минимальную стоимость вина(стоимость должна быть не менее 590 рублей)'
    )
    await state.set_state(FSMFillForm.fill_price_from)


@router.message(StateFilter(FSMFillForm.fill_price_from), lambda x: x.text.isdigit())
async def process_price_from_sent(message: Message, state: FSMContext):
    await state.update_data(price_from = message.text)
    await message.answer(
        text='Укажите максимальную стоимость вина(стоимость должна быть не более 1 999 990 рублей)'
    )
    await state.set_state(FSMFillForm.fill_price_to)

@router.message(StateFilter(FSMFillForm.fill_price_to), lambda x: x.text.isdigit())
async def process_price_to_sent(message: Message, state: FSMContext):
    await state.update_data(price_to = message.text)
    data_to_wine = await state.get_data()
    await state.clear()
    await message.answer(text='Данные загружаются...')

    args = data_to_wine['food']
    prc_from = str(data_to_wine['price_from'])
    prc_to = str(data_to_wine['price_to']) 
    bd_wine(prc_from, prc_to, args)
    connection = create_conection()
    bd_output = execute_read_query(connection, output_wine)

    if len(bd_output) > 0:
        for w in bd_output:
            w1 = ' '.join(w[:2]) + '\n' + ', '.join(w[2:5]) + '\n' + w[5]
            await message.answer(text=w1)

        await message.answer(
            text = 'Для возврата в меню нажмите кнопку',
            reply_markup=create_pagination_keyboard(
                'menu'
            )
        )
    
    else:

        await message.answer(
            text = 'К сожалению, в данном диапозоне нет вина, подходящего к выбранному блюду. Пожалуйста, укажите другой диапозон цен.',
            reply_markup=create_pagination_keyboard('questions')
        )
        






