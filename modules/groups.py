import datetime
from .base import Base

class Groups(Base):
    def __init__(self):
        super().__init__()
    
    def get_group(self, group_id) -> dict:
        """Get information about a group"""
        response = self.get(f'group/{group_id}')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get group information," + response.text)