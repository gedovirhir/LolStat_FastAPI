QUEUEMODES_ENUM = [
    "RANKED_SOLO_5x5",
    "RANKED_FLEX_SR",
    "RANKED_FLEX_TT"
]

TIER_ENUM = [
    'DIAMOND',
    'PLATINUM',
    'GOLD',
    'SILVER',
    'BRONZE',
    'IRON'
]

DIVISION_ENUM = [
    'I',
    'II',
    'III',
    'IV'
]

REGION_ENUM = [
    'br1',
    'eun1',
    'euw1',
    'jp1',
    'kr',
    'la1',
    'la2',
    'na1',
    'oc1',
    'tr1',
    'ru',
    'ph2',
    'sg2',
    'th2',
    'tw2',
    'vn2',
]

#https://static.developer.riotgames.com/docs/lol/queues.json
QUEUEIDS = [
    420, # 5v5 Ranked
    440 # 5v5 Flex ranked
]

SUMMONER_NAME_REGEX = r"^(?!_)\w.*"

ACCOUNTID = 'accountId'
PUUID = 'puuid'
SUMMONERID = 'summonerId'
NAME = 'name'
ID = 'id'
REGION = 'region'

PLAYER_IDENTITY_FIELDS = [
        SUMMONERID,
        NAME,
        ACCOUNTID,
        PUUID,
    ]

