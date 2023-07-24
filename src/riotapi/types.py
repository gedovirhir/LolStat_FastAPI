from enum import Enum
from pydantic import constr

from .enums import (QUEUEMODES_ENUM,
                               DIVISION_ENUM,
                               TIER_ENUM, 
                               REGION_ENUM,
                               QUEUEIDS,
                               PLAYER_IDENTITY_FIELDS)

from src.utils.service import get_mapping

__get_mapping = get_mapping

Q_mode = Enum('Q_mode', __get_mapping(QUEUEMODES_ENUM))
Q_id = Enum('Q_id', __get_mapping(QUEUEIDS))
Div = Enum('Div', __get_mapping(DIVISION_ENUM))
Tier = Enum('Tier', __get_mapping(TIER_ENUM))
Region = Enum('Region', __get_mapping(REGION_ENUM))
Player_identity_field = Enum('Player_identity_field', __get_mapping(PLAYER_IDENTITY_FIELDS))
