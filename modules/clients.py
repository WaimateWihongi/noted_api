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
    
    def search_clients(self, query:str, size:int) -> dict:
        """Search for clients"""
        args = {
            'activeonly': 'true', # Only return active clients
            'searchterm': query, # The search query
            'size': size, # The number of results to return
        }
        
        url = 'clients/search?' + '&'.join([f'{key}={value}' for key, value in args.items()])
        response = self.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not search for clients," + response.text)
    