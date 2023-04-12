import telebot
from christian_calendar.requests_by_token import get_text_by_id, get_holiday_by_id
from christian_calendar.vars import text_id_api_christ_calendar
from excel_utils.open_check_funcs import data_to_json, data_from_json
from utils.logger import logger


def parsing_info_from_site(message: telebot.types.Message, file_from: str, file_to: str):
    """
    Функция для анализа файла со всей информацией полученной от API и парсинг только полезной и заранее выбранной
    информации в отдельный файл
    param file_json: Файл с изначальной информацией
    param file_to: Файл куда будут записаны новые данные
    """
    
    logger.info('Запущена функция get_usefull_info.parsing_info_from_site',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    all_day_info = data_from_json(file_from)
    
    new_info = {'saints_icons': {},
                'texts': {},
                'holidays': []}
    
    for i_item in all_day_info:
        if i_item['abstractDate']['texts']:
            if not text_id_api_christ_calendar[i_item['abstractDate']['texts'][0]['type']] in new_info['texts'].keys():
                new_info['texts'].update({
                    text_id_api_christ_calendar[i_item['abstractDate']['texts'][0]['type']]:
                        list()
                })
            new_info['texts'][text_id_api_christ_calendar[i_item['abstractDate']['texts'][0]['type']]].append(
                get_text_by_id(message=message, text_id=i_item['abstractDate']['texts'][0]['id'])
            )
        
        if i_item['abstractDate']['holidays']:
            new_info['holidays'].append(get_holiday_by_id(message=message,
                                                          holiday_id=i_item['abstractDate']['holidays'][0]['id']))
        
        if i_item['abstractDate']['saints']:
            
            if i_item['abstractDate']['saints'][0]['icons']:
                
                if i_item['abstractDate']['saints'][0]['churchTitle'] and \
                        i_item['abstractDate']['saints'][0]['typeOfSanctity']:
                    
                    if i_item['abstractDate']['saints'][0]['churchTitle']['title'] is not None and \
                            i_item['abstractDate']['saints'][0]['typeOfSanctity']['title'] is not None:
                        
                        new_info['saints_icons'].update({
                            '{typeOfSanctity} {name} ({churchTitle})'.format(
                                typeOfSanctity=i_item['abstractDate']['saints'][0]['typeOfSanctity']['title'],
                                name=i_item['abstractDate']['saints'][0]['title'],
                                churchTitle=i_item['abstractDate']['saints'][0]['churchTitle']['title']):
                                    i_item['abstractDate']['saints'][0]['icons'][0]['original_absolute_url']
                        })
                    
                    elif not i_item['abstractDate']['saints'][0]['churchTitle']:
                        new_info['saints_icons'].update({
                            '{typeOfSanctity} {name}'.format(
                                typeOfSanctity=i_item['abstractDate']['saints'][0]['typeOfSanctity']['title'],
                                name=i_item['abstractDate']['saints'][0]['title']):
                                    i_item['abstractDate']['saints'][0]['icons'][0]['original_absolute_url']
                        })
                    
                    elif not i_item['abstractDate']['saints'][0]['typeOfSanctity']:
                        new_info['saints_icons'].update({
                            '{name} ({churchTitle})'.format(
                                name=i_item['abstractDate']['saints'][0]['title'],
                                churchTitle=i_item['abstractDate']['saints'][0]['churchTitle']['title']):
                                    i_item['abstractDate']['saints'][0]['icons'][0]['original_absolute_url']
                        })
                    
                    else:
                        new_info['saints_icons'].update({
                            '{name}'.format(
                                name=i_item['abstractDate']['saints'][0]['title']):
                                    i_item['abstractDate']['saints'][0]['icons'][0]['original_absolute_url']
                        })
    data_to_json(file_to, new_info)
    logger.info('Создан файл {}'.format(file_to),
                username=message.from_user.username,
                user_id=message.chat.id)
