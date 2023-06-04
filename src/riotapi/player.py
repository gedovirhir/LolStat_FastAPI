from .async_handler import AsyncLolWatcher

class Player(AsyncLolWatcher):
    
    @classmethod
    async def search(self, my_region: str, **kwargs) -> list:
        """
        Gets players for a name/id/accountid/puuid
        
        Args:
            my_region (_str_): region (ru, kr, jp1, br1, eun1 and etc.)
            id= (_list_): list or one of ids of players
            name= (_list_): ... names of players
            account_id= (_list_): ...
            puuid= (_list_): ...
        """
        searchMethod = {
            'id' : self._lwatcher.summoner.by_id,
            'name' : self._lwatcher.summoner.by_name,
            'account_id' : self._lwatcher.summoner.by_account,
            'puuid' : self._lwatcher.summoner.by_puuid
        }
        
        mainMethod = None
        id_info = None
        for m in searchMethod:
            if m in kwargs and kwargs[m]:
                mainMethod = searchMethod[m]
                id_info = kwargs[m]
                break
        
        if not mainMethod: raise TypeError('get_players_by() missed identifying information (id/name/account_id/puuid).\nUse id=*id* and other.')
        
        if not isinstance(id_info, list): id_info = [id_info]
        
        players = []
        for id in id_info:
            try:
                plr_info = mainMethod(my_region, id)
                plr_info.update(
                    {'region' : my_region}
                )
                players.append(
                    player(
                        plr_info['id'],
                        self._lwatcher,
                        plr_info
                    )
            )
            except HTTPError:
                players.append(None)
        
        return players