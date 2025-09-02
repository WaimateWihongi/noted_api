# Noted API

The `noted_api` package provides a Python interface for interacting with the Noted API (https://app.noted.com). It includes modules for managing clients, client lists, users, records, keyworkers, groups, and billing.

## Installation

Ensure you have Python 3.10 installed. Clone the `noted_api` repository from GitHub and install it:

```bash
git clone https://github.com/WaimateWihongi/noted_api.git
cd noted_api
pip install .
```

## Usage

### Initialization

To use the API, initialize the `API` class and log in:

```python
from noted_api import API

api = API()
api.login(username="your_username", password="your_password")
```

### Available Modules

The `API` class combines functionality from the following modules:

- **Clients**: Manage clients and their teams.
- **ClientLists**: Retrieve and manage client lists.
- **Users**: Manage user accounts.
- **Records**: Access and manage records.
- **Keyworkers**: Manage keyworkers.
- **Groups**: Handle group-related operations.
- **Billing**: Manage billing information.

### Example: Managing Clients

```python
# Get client information
client_info = api.get_client(client_id="12345")

# Search for clients
search_results = api.search_clients(query="John Doe")

# Add a client to a team
response = api.add_client_to_team(client_id="12345", team_id="67890")
```

### Example: Managing Client Lists

```python
# Get a specific client list
client_list = api.get_client_list(list_id=1)
```

## Error Handling

All methods raise exceptions if the API request fails. Ensure you handle exceptions appropriately:

```python
try:
    client_info = api.get_client(client_id="12345")
except Exception as e:
    print(f"Error: {e}")
```

## Contributing

This project is no longer actively maintained. However, you are welcome to fork the repository and make modifications as needed. Contributions to your forked version are encouraged!

## License

This package is proprietary and intended for internal use only.
