from .base import Base
from datetime import datetime, timezone

class Records(Base):
    def __init__(self):
        super().__init__()
    
    def get_records_from_client(self, clientid:int, page=0) -> dict:
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
    
    def edit_record_access(self, record_id:int, access_id:int, access:bool) -> dict:
        """Edit the access of a record
        @param record_id: The ID of the record
        @param access_id: The ID of the access (automatically detects if it is a team or user)
        @param access: Grant access or deny access
        """
        URL = f'team/records/{record_id}/rules'
        data = [
            {
                "access": 1,
                "condition": {
                    "type": "TEAM" if len(str(access_id)) <= 3 else "USER",
                    "dataId": access_id,
                    "data":{"id": access_id}
                }
            }
        ]
        if access:
            response = self.post(URL, json=data)
        else:
            response = self.delete(URL, json=data)
        
    def create_record(self, client_id:int, team_id:int) -> dict:
        """Create a record"""
        URL = "records"
        # Get current date and time in UTC
        current_utc_datetime = datetime.utcnow()

        # Convert to ISO 8601 format
        iso8601_utc_datetime = current_utc_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        DATA = {
            "clientCreated": iso8601_utc_datetime,
            "clientId": client_id,
            "content": """{"model":{},"formengine":{"NAME":"Schema UI","VERSION":"beta1"}}""",
            "description": "",
            "form": {
                "id": 3087,
                "name": "Main",
                "visible": True,
                "status": "LIVE",
                "type": "CONSULTATION",
                "modalityId": 83,
                "created": "2019-11-28T23:18:53Z",
                "updated": "2021-04-30T03:58:43Z",
                "mappingId": "NOTED-MN-01",
                "default":False
            },
            "formTypeLabel": "Record",
            "modalityId": 83,
            "patientId": client_id,
            "questions": [],
            "status": "DRAFT",
            "teamId": team_id,
            "type": "CONSULTATION",
            "version": 0,
        }
        response = self.post(URL, json=DATA)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not create record," + response.text)
        
    def get_record(self, record_id:int) -> dict:
        """Get a record"""
        URL = f'records/{record_id}'
        response = self.get(URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get record," + response.text)
    
    def edit_record(self, record_id:int, data:dict) -> dict:
        """Edit a record"""
        URL = f'records/{record_id}'
        response = self.put(URL, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not edit record," + response.text)
    
    def amend_record(self, record_id:int) -> dict:
        """Amend a record"""
        URL = f'records/{record_id}/amend'
        _record_data = self.get_record(record_id)
        _user_data = self.me()
        _record_data["user"] = _user_data
        response = self.put(URL, json=_record_data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not amend record," + response.text)
    
    def delete_record(self, record_id:int) -> dict:
        """Delete a record"""
        URL = f'records/{record_id}'
        response = self.delete(URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not delete record," + response.status_code)
    
    def reassign_record(self, record_id:int, user_id:int) -> dict:
        """Reassign a record to specified user"""
        URL = f'records/{record_id}/reassign'
        DATA = {
            "userId": user_id
        }
        response = self.put(URL, json=DATA)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not reassign record," + response.text)