import datetime
from .base import Base

class Clients(Base):
    def __init__(self):
        super().__init__()

    def get_client(self, client_id:str) -> dict:
        """Get information about a client"""
        response = self.get(f'clients/{client_id}')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get client information," + response.text)
    
    def search_clients(self, query:str, size=10) -> dict:
        """Search for clients"""
        args = {
            'activeonly': 'true', # Only return active clients
            'searchterm': query, # The search query
            'size': size, # The number of results to return
        }
        
        url = 'clientsearch?' + '&'.join([f'{key}={value}' for key, value in args.items()])
        response = self.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not search for clients," + response.text)
    
    def get_client_tags(self, client_id:str) -> dict:
        """Get tags for a client"""
        response = self.get(f'client-tags/client/{client_id}')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get client tags," + response.text)
    
    def search_with_filter(self, filters,
        page=0,
        options={
            "inactiveClients": False,
            "size": 15,
            "sortattr": "dateOfBirth",
            "sortdir": "ASC",
            "timeZone": "Pacific/Auckland"
        }):
        """Search for clients with filters"""
        url = 'clients-search'
        response = self.post(url, json={"filters": filters, "options": {**options, "page": page}})

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not search for clients," + response.text)
        
    def get_clients_in_team(self, team_id:str, page=0, size=15, default_team=False) -> dict:
        """Get clients in a team
        @param team_id: The ID of the team
        @param page: The page number
        @param size: The number of results to return
        @param default_team: Whether clients are in the default team, None for both.
        """
        URL = f'clients'
        params = {
            'inTeams': team_id,
            'page': page,
            'size': size
        }

        # Default Team
        if default_team == False:
            params['andNotInTeam'] = 3174
        elif default_team == True:
            params['andInTeams'] = 3174

        response = self.get(URL, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get clients in team," + response.text)
    
    def get_clients_not_in_team(self, team_id:str, page=0, size=15) -> dict:
        """Get clients not in a team - DEFAULT = 3174
            @param team_id: The ID of the team
            @param page: The page number
            @param size: The number of results to return
            @param default_team: Whether clients are in the default team, None for both.
        """
        URL = f'clients'
        params = {
            'notInTeam': team_id,
            'page': page,
            'size': size
        }

        response = self.get(URL, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get clients not in team," + response.text)
    
    def add_client_to_team(self, client_id:str, team_id:str) -> dict:
        """Add a client to a team"""
        response = self.post(f'team/{team_id}/clients', json=[client_id])
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not add client to team," + response.text)
    
    def filter_clients(self, filters, page=0, size=15) -> dict:
        """Filter clients"""
        response = self.post('advanced-clients-search', json={
            'filters': filters,
            'options': {
                'inactiveClients': False,
                'page': page,
                'size': size,
                'sortattr': 'created',
                'sortdir': 'DESC',
                'timeZone': 'Pacific/Auckland',
            }
        })
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not filter clients," + response.text)
    