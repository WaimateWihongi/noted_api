from .base import Base

class Users(Base):
    def __init__(self):
        super().__init__()
    
    def me(self):
        """Get information about the currently logged in user"""
        response = self.get('users/me')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get user information," + response.text)
    
    def get_all_users(self):
        """Get information about all users"""
        query = """
            query
                usersQuery ($input: UserQueryParams!) {
                users (input: $input) {
                    results {
                    id
                    authenticationDetails {
                        username
                    }
                    firstName
                    lastName
                    email
                    suspended
                    }
                    pages
                }
                }
        """
        data = {
            "query": query,
            "variables": {
                "input": {
                    "searchTerm": "",
                    "sortDir": "desc",
                    "sortAttr": "firstName",
                    "securityRole": "",
                    "activeOnly": False,
                    "size": 25,
                    "page": 100
                }
            }
        }

        response = self.post('graphql', json=data)
        if response.status_code == 200:
            #print(response.json())
            return response.json()["data"]["users"]["results"]
        else:
            raise Exception("Could not get user information," + response.text)
        
    def get_user(self, user_id:str) -> dict:
        """Get information about a user"""
        json_data = {
            "query": "query getUser($id:Long!){user(id:$id){...UserDetails}}fragment UserDetails on User{id authenticationDetails{username}title firstName lastName name gender registrationNumber phone email shortCode suspended notAllowedToDelete isAdminUser securityRoles{id name key}services{id name}privileges{id name key}deleted}}",
            "variables":{"id": user_id}
        }
        response = self.get('users/' + user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get user information," + response.text)
    