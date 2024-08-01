from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove, TelegramObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
import asyncio
from typing import Callable, Dict, Any, Awaitable

from config import TG_TOKEN, ADMIN_ID
from keyboard import *
import db
from words import *


bot = Bot(TG_TOKEN)
dp = Dispatcher()


class Text(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]):
        try:
            curr_buttons = eval(db.get_data_from_db(event.from_user.id, 'buttons')[0][0])
            if event.text is not None: curr_buttons.append(event.text)
            db.update_db(event.from_user.id, ('buttons',),  (str(curr_buttons),))
        except Exception as e:
            print(e)
        return await handler(event, data)
    

class Reg(StatesGroup):
    main = State()
    buttons = State()


class Form(StatesGroup):
    start = State()
    number_of_rooms = State()
    region = State()
    photos = State()


class FAQ(StatesGroup):
    main = State()
    main2 = State()


class Sender(StatesGroup):
    text = State()
    photo = State()
    confirm = State()
    

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(start_message, reply_markup=contact_keyboard(message.from_user.id))
    
    
@dp.message(F.text == 'Начать работу с GetFlat')
async def menu(message: Message, state: FSMContext):
    await message.answer('Расскажите о ваших апартаментах, ответив всего на 3 вопроса ⭐')
    await state.set_state(Form.start)
    await asyncio.sleep(0.5)
    await asyncio.create_task(start_form(message, state))


@dp.message(F.text == 'Связаться с GetFlat')
async def chat(message: Message, state: FSMContext):
    await message.answer('@wegetflat')


@dp.message(F.contact)
async def contact(message: Message, state: FSMContext, back = False):
    if back:
        await message.answer('С GetFlat вы сможете увеличить доход от аренды до +30% 📈', reply_markup=main_keyboard())
        await state.set_state(Reg.main)
    elif message.contact is not None and message.contact.user_id == message.from_user.id:
        await message.answer('С GetFlat вы сможете увеличить доход от аренды до +30% 📈', reply_markup=main_keyboard())
        await state.set_state(Reg.main)
        db.insert_user_to_db(message.from_user.id)
        db.update_db(message.from_user.id, ('number','username','name'), (f'+{message.contact.phone_number}', f'@{message.from_user.username}', message.from_user.full_name))

        for id in ADMIN_ID:
            try:
                await bot.send_message(id, text=f'Отправлена заявка: \n{message.from_user.full_name}  @{message.from_user.username} +{message.contact.phone_number}')
            except Exception as e:
                print(e)       

    else:
        await message.answer(incorrect_contact_message)

@dp.message(F.text == 'Создать рассылку')
async def sender(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_ID:
        return
    
    await message.answer('Введите текст рассылки', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Sender.text)


@dp.message(Sender.text, F.text)
async def sender_text(message: Message, state: FSMContext):
    await state.update_data(text = message.text)
    await message.answer('Отправьте изображение, или нажмите "Нет фото"', reply_markup=no_photo_keyboard())
    await state.set_state(Sender.photo)


@dp.message(Sender.photo, F.text == 'Нет фото')
async def sender_no_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Подтвердите рассылку данного сообщения:', reply_markup=confirm_keyboard())
    await message.answer(data['text'])
    await state.set_state(Sender.confirm)


@dp.message(Sender.photo, F.photo)
async def sender_photo(message: Message, state: FSMContext):
    await state.update_data(photo = message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer('Подтвердите рассылку данного сообщения:', reply_markup=confirm_keyboard())
    await message.answer_photo(photo=message.photo[-1].file_id, caption=data['text'])
    await state.set_state(Sender.confirm)


@dp.message(Sender.confirm, F.text == 'Подтвердить')
async def sender_yes(message: Message, state: FSMContext):
    data = await state.get_data()

    for id in db.get_users_from_db('user_id'):
        try:
            if 'photo' not in data:
                await bot.send_message(id[0], data['text'])
            else:
                await bot.send_photo(id[0], photo=data['photo'], caption=data['text'])

        except Exception as e:
            print(e)
        await asyncio.sleep(1)

    await message.answer('Рассылка завершена', reply_markup=contact_keyboard(message.from_user.id))
    await state.clear()

@dp.message(Sender.confirm, F.text == 'Отменить')
async def sender_no(message: Message, state: FSMContext):
    await message.answer('Рассылка отменена', reply_markup=contact_keyboard(message.from_user.id))
    await state.clear()


@dp.message(F.text == show_applications_button_text)
async def show_forms(message: Message):
    if message.from_user.id not in ADMIN_ID:
        return  
    try:
        for name, username, number, form, buttons in db.get_users_from_db('name, username, number, form, buttons'):
            if form is None or len(form) == 0:
                await message.answer(f'Имя: {name}\n\nТелеграм: {username}\n\nНомер телефона: {number}\n\nАнкета не заполнена')
            else:
                form = eval(form)
                buttons = eval(buttons)
                await message.answer(f'Имя: {name}\n\nТелеграм: {username}\n\nНомер телефона: {number}\n\nКоличество комнат: {form.get("number_of_rooms")}\n\nРайон: {form.get("region")}\n\nИстория кнопок: {" > ".join(buttons)}')
                if len(form['photos']) > 1:
                    for photo in form['photos']:
                        await message.answer_photo(photo)
                        await asyncio.sleep(0.2)
            await asyncio.sleep(0.5)
    except Exception as e:
        await message.answer(no_applications_message)
        print(e)


@dp.message(F.text == 'Подробнее об условиях')
@dp.message(Reg.main)
async def menu(message: Message, state: FSMContext, back = False):
    if message.text in ('Начать работу с GetFlat', 'Вернуться назад'):
        await message.answer('Расскажите о ваших апартаментах, ответив всего на 3 вопроса:', reply_markup=form_keyboard0())
        await state.set_state(Form.start)

    elif message.text in ('Узнать подробнее', 'Вернуться к вопросам', 'Подробнее об условиях'):
        if message.text == 'Подробнее об условиях':
            await state.set_state(FAQ.main2)
            form = True
        else:
            form = False
            await state.set_state(FAQ.main)
        await message.answer('''Здесь вы сможете узнать ответы на самые распространенные вопросы👇 ''',
                             reply_markup=faq_main_keyboard(form))


@dp.message(FAQ.main)
async def q(message: Message, state: FSMContext):
    
    form = False

    if message.text == 'Назад':
        await message.answer('''Здесь вы сможете узнать ответы на самые распространенные вопросы👇 ''',
                             reply_markup=faq_main_keyboard(form))
        await state.set_state(FAQ.main)


    if message.text == 'Что такое GetFlat и как это работает? ':
        await message.answer('GetFlat - это сервис по управлению и сдаче апартаментов в краткосрочную аренду нового поколения. Мы помогаем владельцам зарабатывать пассивно без лишнего стресса', reply_markup=faq_keyboard3())

    elif message.text == 'Коммисия и условия работы':
        await message.answer('''В GetFlat вы можете выбрать 1 из 3 типов контрактов, с комиссиями от 16 до 20%. Каждый контракт включает в себя множество сервисов:

▪️Размещение рекламы и привлечение гостей 
▪️Управление бронированиями и обработка запросов
▪️Уборка, тех. обслуживание и оплата счетов
▪️Формирование отчетов и зачисление выплат''', reply_markup=faq_keyboard2(form))

    elif message.text == 'Получение выплат':
        await message.answer('Выплаты и отчеты личный менеджер отправляет в начале каждого месяца, на указанный в контракте банковский счет и почту. Также владельцы могут отслеживать работу своих апартаментов в личном кабинете.', reply_markup=faq_keyboard2(form))

    elif message.text == 'Про районы':
        await message.answer('''Наиболее популярные для  посуточной аренды районы в Дубае: 
▪️Palm Jumeirah
▪️JBR
▪️Marina
▪️Downtown & Business Bay
▪️Dubai Harbour
Не волнуйтесь если апартаменты находятся в другом районе, Getflat заставит их работать !''', reply_markup=faq_keyboard2(form))

    elif message.text == 'Безопасность  апартаментов':
        await message.answer('''В GetFlat мы серьезно относимся к безопасности и принимаем различные меры для сохранности апартаментов:
▪️Взимаем депозит при заселении
▪️Обеспечиваем экстренную поддержку 24/7
▪️Проводим систематические проверки апартаментов до и после проживания гостей
▪️Проверяем документы при бронировании''', reply_markup=faq_keyboard2(form))

    elif message.text == 'Личное пользование':
        await message.answer('В GetFlat вы можете забронировать свою недвижимость для личного проживания в любое время в течение года при условии отсутствия бронирований', reply_markup=faq_keyboard2(form))


@dp.message(FAQ.main2)
async def q(message: Message, state: FSMContext):
    
    form = True

    if message.text == 'Назад':
        await message.answer('''Здесь вы сможете узнать ответы на самые распространенные вопросы👇 ''',
                             reply_markup=faq_main_keyboard(form))
        await state.set_state(FAQ.main2)


    if message.text == 'Что такое GetFlat и как это работает? ':
        await message.answer('GetFlat - это сервис по управлению и сдаче апартаментов в краткосрочную аренду нового поколения. Мы помогаем владельцам зарабатывать пассивно без лишнего стресса', reply_markup=faq_keyboard3())

    elif message.text == 'Коммисия и условия работы':
        await message.answer('''В GetFlat вы можете выбрать 1 из 3 типов контрактов, с комиссиями от 16 до 20%. Каждый контракт включает в себя множество сервисов:

▪️Размещение рекламы и привлечение гостей 
▪️Управление бронированиями и обработка запросов
▪️Уборка, тех. обслуживание и оплата счетов
▪️Формирование отчетов и зачисление выплат''', reply_markup=faq_keyboard2(form))

    elif message.text == 'Получение выплат':
        await message.answer('GetFlat - это сервис по управлению и сдаче апартаментов в краткосрочную аренду нового поколения. Мы помогаем владельцам зарабатывать пассивно без лишнего стресса', reply_markup=faq_keyboard2(form))

    elif message.text == 'Про районы':
        await message.answer('''Наиболее популярные для  посуточной аренды районы в Дубае: 
▪️Palm Jumeirah
▪️JBR
▪️Marina
▪️Downtown & Business Bay
▪️Dubai Harbour
Не волнуйтесь если апартаменты находятся в другом районе, Getflat заставит их работать !''', reply_markup=faq_keyboard2(form))

    elif message.text == 'Безопасность  апартаментов':
        await message.answer('''В GetFlat мы серьезно относимся к безопасности и принимаем различные меры для сохранности апартаментов:
▪️Взимаем депозит при заселении
▪️Обеспечиваем экстренную поддержку 24/7
▪️Проводим систематические проверки апартаментов до и после проживания гостей
▪️Проверяем документы при бронировании''', reply_markup=faq_keyboard2(form))

    elif message.text == 'Личное пользование':
        await message.answer('В GetFlat вы можете забронировать свою недвижимость для личного проживания в любое время в течение года при условии отсутствия бронирований', reply_markup=faq_keyboard2(form))


@dp.message(Form.start)
async def start_form(message: Message, state: FSMContext, back = False):
    if message.text == 'Вернуться назад' and not back:
        await state.set_state(Reg.main)
        await asyncio.create_task(contact(message, state, True))
        return
    
    await message.answer('''1. Какое количество комнат в ваших апартаментах? 

Выберите или напишите свой вариант👇''', reply_markup=form_keyboard1())
    await state.set_state(Form.number_of_rooms)


@dp.message(Form.number_of_rooms)
async def number_of_rooms(message: Message, state: FSMContext, back = False):
    if message.text == 'Вернуться назад' and not back:
        await state.set_state(Reg.main)
        await asyncio.create_task(contact(message, state, True))
        return

    if message.text != 'Вернуться назад': await state.update_data(number_of_rooms = message.text) 
    await message.answer('''2. В каком районе находятся апартаменты? 

Выберите или напишите свой вариант👇''', reply_markup=form_keyboard2())
    await state.set_state(Form.region)


@dp.message(Form.region)    
async def region(message: Message, state: FSMContext, back = False):
    if message.text == 'Вернуться назад' and not back:
        await state.set_state(Form.start)
        await asyncio.create_task(start_form(message, state, True))
        return

    if message.text != 'Вернуться назад': await state.update_data(region = message.text)
    await message.answer('3. Если у вас есть фотографии апартаментов, отправьте их, и нажмите "Приложить фото квартиры" 📷', reply_markup=form_keyboard3())
    await state.set_state(Form.photos)
    await state.update_data(photos = [])


@dp.message(F.photo, Form.photos)    
async def photos(message: Message, state: FSMContext):
    data = await state.get_data()
    data = data['photos']
    data.append(message.photo[-1].file_id)
    await state.update_data(photos = data)


@dp.message(Form.photos)    
async def photos_text(message: Message, state: FSMContext, back = False):
    if message.text == 'Вернуться назад' and not back:
        await state.set_state(Form.number_of_rooms)
        await asyncio.create_task(number_of_rooms(message, state, True))
        return

    data = await state.get_data()
    db.insert_user_to_db(message.from_user.id)
    db.update_db(message.from_user.id, ('form',), (str(dict(data.items())),))
    await message.answer('Спасибо за предоставленную информацию. Ваше обращение уже в пути, менеджер GetFlat свяжется с вами в ближайшее время👩‍💻',
                         reply_markup=form_end())
    await asyncio.create_task(send_form(message))
    await state.clear()


async def send_form(message: Message):
    username, name, number, form = db.get_data_from_db(message.from_user.id, 'username, name, number, form')[0]
    form = eval(form)

    for id in ADMIN_ID:
        try:
            if len(form['photos']) == 0:
                await bot.send_message(id, f'{name}, {username}, {number}, заполнена анкета:\n Количество комнат: {form["number_of_rooms"]}\n Район: {form["region"]}\n Фотографии не приложены.')
            else:
                await bot.send_message(id, f'{name}, {username}, {number}, заполнена анкета:\n Количество комнат: {form["number_of_rooms"]}\n Район: {form["region"]}\n Приложенные фотографии:')
                for i in form['photos']:
                    await bot.send_photo(chat_id=id, photo=i, disable_notification=True)
                    await asyncio.sleep(0.2)
        
            await asyncio.sleep(1)
        except Exception as e:
            print(e)


@dp.message(F.photo)
async def send_photo(message: Message):
    await message.answer(sending_picture_message)
    for id in ADMIN_ID:
        try:
            await bot.send_photo(id, message.photo[-1].file_id, caption=f'@{message.from_user.username} {message.from_user.full_name} отправил изображение.')
        except Exception as e:
            print(e)

