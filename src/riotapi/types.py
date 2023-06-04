from enum import Enum

from src.riotapi.enums import (QUEUEMODES,
                               DIVISION,
                               TIER, 
                               REGION,
                               QUEUEIDS)

def __get_mapping(enum_list: list):
    return zip(enum_list, enum_list)

Q_mode = Enum('Q_mode', __get_mapping(QUEUEMODES))
Q_id = Enum('Q_id', __get_mapping(QUEUEIDS))
Div = Enum('Div', __get_mapping(DIVISION))
Tier = Enum('Tier', __get_mapping(TIER))
Region = Enum('Region', __get_mapping(REGION))
