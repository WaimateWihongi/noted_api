from .base import Base

class ClientLists(Base):
    def __init__(self):
        super().__init__()
    
    def get_client_list(self, list_id: int) -> dict:
        """Get information about a client list"""
        
        # First, get all client lists
        response = self.get(f'advanced-clients-search/queries')
        if response.status_code == 200:
            for i in response.json():
                if i['id'] == list_id:
                    return i
        else:
            raise Exception("Could not get client list information," + response.text)