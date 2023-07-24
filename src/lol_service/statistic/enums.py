import copy
from typing import Any, Tuple, Hashable, Union, List

class DictWithCopyCalled(dict):
    def __getitem__(self, __key: Any) -> Any:
        v = super().__getitem__(__key)
        v = copy.deepcopy(v)
        return v

class FieldNameSpecialSerializer(DictWithCopyCalled):
    
    def _fit_object(
        self, 
        obj: Union[list, dict, Ellipsis, Any],
        value: Any
    ):
        if isinstance(obj, list):
            for i, v in enumerate(obj):
                obj[i] = self._fit_object(v, value)
        
        elif isinstance(obj, dict):
            for k, v in obj.items():
                obj[k] = self._fit_object(v, value)
        
        elif obj is ...:
            return value
        
        return obj
        
    def _decompose_object(self, obj: Union[list, dict, Any]) -> Union[List[str], str]:
        """
        dict[str, ...] -> str
        
        """
        if isinstance(obj, list):
            for i, v in enumerate(obj):
                obj[i] = self._decompose_object(v)

            return obj

        elif isinstance(obj, dict):
            res = []
            for k, v in obj.items():
                if not isinstance(v, (list, dict)):
                    res.append(k)
                else:
                    res.append(self._decompose_object(obj[k]))
            
            if len(res) == 1:
                return res[0]
            else:
                return res
        
        else:
            return obj
    
    def __getitem__(
        self, 
        __key: Union[
            Tuple[Hashable, Any],
            Hashable
        ]
    ) -> Any:
        if isinstance(__key, tuple):
            obj = super().__getitem__(__key[0])
            return self._fit_object(obj, __key[1])

        elif isinstance(__key, Hashable): # -> str | List[str]
            value = super().__getitem__(__key)
            return self._decompose_object(value)
        else:
            raise ValueError

P = "info.participants"
fields_manager = FieldNameSpecialSerializer(
    {
        "Puuid": {"metadata.participants": ...},
        "Players": {P: ...},
        "Item": {
            "$or": [
                {f"{P}.item{v}": ...} for v in range(0,7)
            ],
        },
        "GameDuration": {"info.gameDuration": ...},
        "Assists": {f"{P}.assists": ...},
        "ChampLevel": {f"{P}.champLevel": ...}, 
        "ChampionName": {f"{P}.championName": ...}, 
        "Deaths": {f"{P}.deaths": ...}, 
        "Kills": {f"{P}.kills": ...}, 
        "TotalDamage": {f"{P}.totalDamageDealt": ...}, 
        "DamageToBuildings": {f"{P}.damageDealtToBuildings": ...}, 
        "DamageToObjectives": {f"{P}.damageDealtToObjectives": ...}, 
        "Position": {f"{P}.individualPosition": ...}, 
        "Win": {f"{P}.win": ...}, 
    }
)
FIELD_NAMES = list(fields_manager.keys())
GROUP_FIELDS = [
    "Players"
]
AGGREGATION_NAMES = [
    "addToSet",
    "avg",
    "bottom",
    "bottomN",
    "count",
    "first",
    "firstN",
    "last",
    "lastN",
    "max",
    "maxN",
    "mergeObjects",
    "min",
    "push",
    "stdDevPop",
    "stdDevSamp",
    "sum",
    "top",
    "topN",
]

ITEMS = [
    3114, 1018, 3110, 8020, 7007, 6692, 6616, 1083, 7018, 1006, 6696, 6670, 3001, 6656, 2015, 4005, 7025, 7031, 3123, 3033, 3864, 4644, 4630, 2421, 3191, 3044, 3020, 3155, 7029, 7027, 3076, 1033, 3100, 3078, 3152, 3116, 3115, 3121, 4637, 1001, 2065, 3803, 1058, 3801, 3035, 3193, 3036, 3153, 3083, 3047, 3095, 1004, 3094, 1036, 4642, 3066, 4638, 3053, 6667, 3157, 3211, 7002, 4635, 3046, 3177, 6694, 3031, 3184, 6693, 4628, 3004, 2422, 3111, 3140, 6676, 6672, 3057, 3124, 3067, 4636, 3041, 3087, 3748, 6653, 3109, 6620, 7012, 3086, 3858, 1026, 3085, 3179, 7016, 4643, 7006, 3504, 2420, 2424, 1101, 1082, 1052, 3508, 3916, 6630, 2033, 3068, 1053, 3850, 3026, 4633, 3012, 7009, 3190, 3108, 3134, 1043, 3814, 3077, 1055, 2403, 6665, 6035, 2003, 3142, 7011, 7028, 3117, 3040, 6655, 1031, 7032, 3158, 1029, 3802, 3003, 2031, 3222, 2423, 1028, 2051, 4632, 3071, 4401, 3070, 7015, 6673, 6662, 4645, 3089, 3075, 6657, 3112, 3102, 1038, 6632, 1027, 6609, 6631, 6677, 1103, 1056, 1057, 0, 3165, 3156, 3084, 6691, 3009, 3860, 3133, 6675, 3074, 3135, 1054, 6333, 3853, 3105, 3742, 7026, 3006, 3072, 1011, 1042, 6617, 3113, 3024, 2010, 1102, 1037, 3082, 8001, 6029, 2139, 2055, 3042, 7000, 6671, 3011, 3145, 3051, 3107, 3023, 3859, 4629, 7020, 3181, 6660, 7013, 3855, 3119, 3143, 7030, 3139, 3161, 3851, 6664, 3091, 3050, 3065, 6695, 3857
]