import datetime
from .base import Base

class Keyworkers(Base):
    def __init__(self):
        super().__init__()
    
    def get_keyworkers(self, client_id) -> dict:
        """Get the keyworkers of a client
        @param client_id: The ID of the client
        """
        response = self.get(f'key-worker-relationships?clientId={client_id}')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get keyworkers," + response.text)
    
    def add_keyworker(self, client_id, keyworker_id, start_date=datetime.datetime.now().isoformat()) -> bool:
        """Add the keyworker to a client.
        @param client_id: The ID of the client
        @param keyworker_id: The ID of the keyworker
        """

        # Check if the keyworker is already set
        keyworkers = self.get_keyworkers(client_id)
        if keyworker_id in [x["user"]["id"] for x in keyworkers]:
            return True
        
        # Check if the keyworker exists
        try:
            self.get_user(keyworker_id)
        except:
            raise Exception("Could not set keyworker, keyworker does not exist!")

        json_data = {
            "client": {"id": client_id},
            "relationshipStart": f"{start_date}+12:00", # The date the relationship started
            "user": {"id": keyworker_id},
        }
        response = self.post(f'key-worker-relationships/', json=json_data, return_error=True)
        if response.status_code == 201:
            return True
        else:
            raise Exception("Could not set keyworker," + response.text)

    def remove_keyworker(self, client_id, keyworker_id, end_date=datetime.datetime.now().isoformat()) -> bool:
        data = self.get_keyworkers(client_id) # Get the keyworkers
        
        # Check if the keyworker is there.
        if keyworker_id not in [x["user"]["id"] for x in data]:
            raise Exception("Could not remove keyworker, keyworker is not set!")
        data = [x for x in data if x["user"]["id"] == keyworker_id][0] # Get the keyworker data
        
        data["relationshipEnd"] = f"{end_date}+12:00" # Set the end date
        response = self.session.put(f'{self.API_URL}key-worker-relationships/{data["id"]}', json=data)

        return response.status_code == 200

    def get_clients_with_keyworker(self, keyworker_id) -> list:
        """Get all clients with a keyworker"""
        json = {
            "filters":[
                {
                    "name": "KEY_WORKER",
                    "matchType": "ANY",
                    "users": [
                        {
                            "id": keyworker_id,
                        }
                    ]
                }
            ],
            "options": {
                "inactiveClients": False,
                "size": 15,
                "page": 0,
                "sortattr": "dateOfBirth",
                "sortdir": "ASC",
                "timeZone": "Pacific/Auckland"
            }
        }
        clients = []
        max_clients = 1_000_000 # The maximum number of clients to get, temporary value...
        while len(clients) < max_clients:
            response = self.post('clients-search', json=json)
            if response.status_code == 200:
                if not response.json()["results"]:
                    break
                clients += response.json()["results"]
            else:
                raise Exception("Could not get clients," + response.text)
            max_clients = response.json()["totalItems"]
            json["options"]["page"] += 1
        return clients
        
                