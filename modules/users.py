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
            "query": '\n    query getUser($id: Long!) {\n  user(id: $id) {\n    ...UserDetails\n  }\n}\n    \n    fragment UserDetails on User {\n  id\n  authenticationDetails {\n    username\n  }\n  title\n  firstName\n  lastName\n  name\n  gender\n  registrationNumber\n  phone\n  email\n  shortCode\n  suspended\n  notAllowedToDelete\n  isAdminUser\n  securityRoles {\n    id\n    name\n    key\n  }\n  services {\n    id\n    name\n  }\n  privileges {\n    id\n    name\n    key\n  }\n  deleted\n}\n    ',
            "variables":{"id": user_id}
        }
        response = self.post('graphql', json=json_data, return_error=True)
        if response.status_code == 200:
            return response.json()["data"]["user"]
        else:
            raise Exception("Could not get user," + response.text)
    