from telebot import types


def IKM_christ_day_bonus(day_bonus: list) -> types.InlineKeyboardMarkup:
    """
    Клавиатура для выбора текста дня.
    :return: Возвращается клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_christ_day_bonus = types.InlineKeyboardMarkup(row_width=1)
    
    for every_bonus in day_bonus:
        ikm_christ_day_bonus.add(types.InlineKeyboardButton(text=every_bonus,
                                                            callback_data=every_bonus)
                                 )
    
    # ikm_christ_day_bonus.add(types.InlineKeyboardButton(text='Вернуться назад',
    #                                                         callback_data='return'))
    
    return ikm_christ_day_bonus

