from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import ADMIN_ID
from words import show_applications_button_text, send_contact_button_text, input_field_placeholder


def contact_keyboard(user_id: int):
    btn = [[KeyboardButton(text=send_contact_button_text, request_contact=True)]]
    if user_id in ADMIN_ID:
        btn.append([KeyboardButton(text=show_applications_button_text)])
        btn.append([KeyboardButton(text='Создать рассылку')])


    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True,
                                   input_field_placeholder=input_field_placeholder)
    
    return keyboard


def main_keyboard():
    btn = [[KeyboardButton(text='Начать работу с GetFlat'), KeyboardButton(text='Узнать подробнее')]]

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def form_keyboard0():
    btn = [[KeyboardButton(text='Поделиться'), KeyboardButton(text='Вернуться назад')]]

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def form_keyboard1():
    btn = [[KeyboardButton(text='Студия'), KeyboardButton(text='1BR'), KeyboardButton(text='2BR'), KeyboardButton(text='3BR')],
           [KeyboardButton(text='Вернуться назад')]]

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def form_keyboard2():
    btn = [[KeyboardButton(text='Palm Jumeirah'), KeyboardButton(text='Downtown'), KeyboardButton(text='Dubai Creek'), KeyboardButton(text='JBR')],
           [KeyboardButton(text='Marina'), KeyboardButton(text='Business Bay'), KeyboardButton(text='Dubai Harbour')],
           [KeyboardButton(text='Вернуться назад')]]

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def form_keyboard3():
    btn = [[KeyboardButton(text='Приложить фото квартиры'), KeyboardButton(text='Нет фото')],
           [KeyboardButton(text='Вернуться назад')]]

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def form_end():
    btn = [[KeyboardButton(text='Подробнее об условиях'), KeyboardButton(text='Связаться с GetFlat')]]

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def faq_main_keyboard(did_form: bool = False):
    btn = [[KeyboardButton(text='Что такое GetFlat и как это работает? '), KeyboardButton(text='Коммисия и условия работы')],
           [KeyboardButton(text='Получение выплат'), KeyboardButton(text='Про районы')],
           [KeyboardButton(text='Безопасность  апартаментов'), KeyboardButton(text='Личное пользование')],
           ]
    if not did_form:
        btn.append([KeyboardButton(text='Начать работу с GetFlat')])

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def faq_keyboard2(did_form: bool = False):
    btn = [[KeyboardButton(text='Начать работу с GetFlat')],
           [KeyboardButton(text='Назад')]]
    if did_form:
        btn = [[KeyboardButton(text='Назад')]]
        
    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def faq_keyboard3():
    btn = [[KeyboardButton(text='Коммисия и условия работы')],
           [KeyboardButton(text='Назад')]]
    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def no_photo_keyboard():
    btn = [[KeyboardButton(text='Нет фото')]]

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard


def confirm_keyboard():
    btn = [[KeyboardButton(text='Подтвердить')], [KeyboardButton(text='Отменить')]]

    keyboard = ReplyKeyboardMarkup(keyboard=btn, 
                                resize_keyboard=True, 
                                one_time_keyboard=True,
                                )
    
    return keyboard
