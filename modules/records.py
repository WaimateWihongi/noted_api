from .base import Base

class Records(Base):
    def __init__(self):
        super().__init__()
    
    def get_records_from_client(self, clientid:int) -> dict:
        """Get all records from a client"""
        params = {
            "page": 0,
            "size": 1000,
            "sortattr": "id",
            "sortdir": "ASC",
        }
        url = 'records/client/' + str(clientid) + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        response = self.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get records from client," + response.text)