from datetime import date
from pydantic import BaseModel, Extra, root_validator, validator, Field
from abc import ABC, abstractmethod

from typing import (List,
                    Union,
                    Optional,
                    Any,
                    )

from src.models import ProjectBase

from .enums import fields_manager
from .types import Aggregation_name, Field_name, Group_field_name

class RequestFieldBase(ProjectBase, ABC):
    @abstractmethod
    def to_mongo(self) -> dict: ...
    
class BaseField(RequestFieldBase):
    field_name: Field_name    

class FilterField(BaseField):
    value: Union[int, str, dict, list]
    
    @property
    def mongo_field(self):
        if isinstance(self.value, list):
            return fields_manager[self.field_name, {"$in": self.value}]
        else:
            return fields_manager[self.field_name, self.value]
    
    def to_mongo(self):
        
        body = {
                "$match": ...
            }
        body["$match"] = self.mongo_field
        
        return body

class GroupField(BaseField):
    field_name: Group_field_name
    filter_fields: "filter_fields_type"

    @property
    def mongo_field(self):
        return fields_manager[self.field_name]

    def to_mongo(self):
        return {"$unwind": f"${self.mongo_field}"}
        
        
field_type = Union[FilterField, GroupField]
filter_fields_type = List[field_type]

GroupField.update_forward_refs()

class Aggregation(RequestFieldBase):
    aggregation_name: Aggregation_name
    field_name: Union[Field_name, int]
    
    @property
    def group_name(self):
        name_ = str(self.field_name)
        return f"{name_.replace('.', '_')}_{self.aggregation_name}"
    
    @property
    def mongo_field(self):
        if isinstance(self.field_name, int):
            field_ = self.field_name
        else:
            field_ = f"${fields_manager[self.field_name]}"
        return {
            self.group_name: {
                f"${self.aggregation_name}": field_
            }
        }
    
    def to_mongo(self):
        
        return self.mongo_field
    
class DateRange(RequestFieldBase):
    date_from: Optional[int]
    date_to: Optional[int]
    
    def to_mongo(self, date_field: str = "info.gameCreation") -> dict:
        if not (self.date_from or self.date_to):
            return {}
        
        mongo_script = {
            "$match": {
                date_field: {
                    "$gte": self.date_from,   
                    "$lte": self.date_to
                }
            }
        }
        
        return mongo_script

class WindowCriteria(RequestFieldBase):
    limit: Optional[int]
    offset: Optional[int]
    
    def to_mongo(self) -> List[dict]:
        mongo_step = [
            {"$offset": self.limit},
            {"$skip": self.offset}
        ]
        
        return mongo_step

class MatchReportRequestSchema(ProjectBase):
    filter_fields: filter_fields_type
    aggregations: List[Aggregation]
    date_range: Optional[DateRange]
    window_criteria: Optional[WindowCriteria]
    
    @validator("aggregations", "filter_fields", always=True)
    def aggr_fields_not_blank(cls, value):
        if not value:
            raise ValueError(f"Can't be blank")
        return value
    
    def _fit_filter_fields(self, fields: filter_fields_type, aggregations_cont: list = []):
        for field in fields:
            aggregations_cont.append(
                field.to_mongo()
            )
                
            if isinstance(field, GroupField):
                self._fit_filter_fields(field.filter_fields, aggregations_cont)
    
    def _fit_aggregations(self, aggregation_cont: list = []):
        body = {
            "_id": "null",
        }
        
        for a in self.aggregations:
            body.update(
                a.to_mongo()
            ) 
        body = {
            "$group": body
        }
        aggregation_cont.append(body)
    
    def _fit_static_field(self, aggregations_cont: list = []):
        if self.date_range:
            aggregations_cont.insert(0,self.date_range.to_mongo())
        
        if self.window_criteria:
            aggregations_cont.extend(
                self.window_criteria.to_mongo()
            )
        
    def to_mongo_script(self):
        aggregation_cont = []
        
        self._fit_filter_fields(self.filter_fields, aggregation_cont)
        
        if self.aggregations:
            self._fit_aggregations(aggregation_cont)
            
        self._fit_static_field(aggregation_cont)
        
        return aggregation_cont

class MatchResponseResponseRow(ProjectBase):
    class Config:
        extra = Extra.allow
    
    @root_validator(pre=True)
    def remove_unwanted_fields(cls, values):
        UNWANTED_FIELDS = ['_id']
        
        for f in UNWANTED_FIELDS:
            if f in values:
                del values[f]
        
        return values

class MatchReportsResponse(ProjectBase):
    info: Optional[List[MatchResponseResponseRow]]
    request_id: str

class ItemRecRequest(ProjectBase):
    champion_name: str
    items: List[int] = Field(max_items=6)
    lane: str

class ItemRecResponse(ProjectBase):
    item_id: int