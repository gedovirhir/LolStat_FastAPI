from typing import Any, Generic, Union

def is_generic_instance(value: Any, generic_type): 
    origin = getattr(generic_type, '__origin__', None)
    args = getattr(generic_type, '__args__', None)
    
    if origin is Union:
        for sub_class in args:
            if is_generic_instance(value, sub_class):
                return True
    
    elif not (origin or args):
        return isinstance(value, generic_type)
    
    elif isinstance(value, origin):
        
        if origin is list:
            for v_i in value:
                if not is_generic_instance(v_i, args[0]):
                    return False
        
        elif origin is dict:
            for item, value in value.items():
                if not (
                    is_generic_instance(item, args[0]) 
                    or is_generic_instance(value, args[1])
                ):
                    return False
        
        elif origin is tuple:
            for item, type_ in zip(value, args):
                if not is_generic_instance(item, type_):
                    return False

        return True
    
    return False

def get_mapping(enum_list: list):
    key_list = [str(i) for i in enum_list]
    
    return zip(key_list, enum_list)