from enum import Enum

from src.utils.service import get_mapping

from .enums import AGGREGATION_NAMES, FIELD_NAMES, GROUP_FIELDS

Aggregation_name = Enum('Aggregation', get_mapping(AGGREGATION_NAMES))
Field_name = Enum('Fields', get_mapping(FIELD_NAMES))
Group_field_name = Enum('Group_field_name', get_mapping(GROUP_FIELDS))
