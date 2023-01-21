import os.path
import time
import urllib.request
import re

from christian_calendar.requests_by_token import get_day_info_func, get_text_by_id
from excel_utils.open_check_funcs import data_from_json
from loader import text_id_api_christ_calendar

all_info_from_site = data_from_json('jsons/all_day_info_fite.json')

def parsing_info_from_site(all_day_info: list):
    new_info = {'saints_icons': {},
                'texts': {},
                'holidays': {}}
    
    for i_item in all_day_info:
        if i_item['abstractDate']['texts']:
            new_info['texts'].update({
                text_id_api_christ_calendar[i_item['abstractDate']['texts'][0]['type']]:
                    get_text_by_id(i_item['abstractDate']['texts'][0]['id'])
            })
            # print('\t {} \t'.format(i_item['abstractDate']['texts'][0]['type']), end='')
            # print(text_id_api_christ_calendar[i_item['abstractDate']['texts'][0]['type']])
            # get_text_by_id(i_item['abstractDate']['texts'][0]['id'])
      
        if i_item['abstractDate']['holidays']:
            
            print(i_item['abstractDate']['holidays'])
      
        if i_item['abstractDate']['saints']:
            if i_item['abstractDate']['saints'][0]['jsons']:
                new_info['saints_icons'].update({
                    i_item['abstractDate']['saints'][0]['title']:
                        i_item['abstractDate']['saints'][0]['jsons'][0]['original_absolute_url']
                })
                # print(i_item['abstractDate']['saints'][0]['title'])
                # print(i_item['abstractDate']['saints'][0]['jsons'][0]['original_absolute_url'])
    print(new_info)

parsing_info_from_site(all_info_from_site)