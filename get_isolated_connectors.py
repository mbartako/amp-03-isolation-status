import requests

# AMP for Endpoint API Credentials
amp_client_id = 'a1b2c3d4e5f6g7h8i9j0'
amp_api_key = 'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6'

# Instatiate a session to be used for the AMP for Endpoints API
session = requests.Session()

# Set the authentication for the session
session.auth = (amp_client_id, amp_api_key)

# AMP URL for collecting connector GUIDs
computers_url = 'https://api.amp.cisco.com/v1/computers'

# Query AMP for Endpoints for connectors
response = session.get(computers_url)

# Decode the JSON response
response_json = response.json()

# Name the 'data' list in the JSON response
data = response_json['data']

# Container for holding the GUIDs
isolated_connectors = {}

# Iterate over the response data
for connector in data:
    # Name the elements from the connector that are needed
    isolation = connector.get('isolation', {})
    available = isolation.get('available')
    status = isolation.get('status')
    connector_guid = connector.get('connector_guid')
    hostname = connector.get('hostname')

    # Check if the connector has isolation available and is isolated
    if available and status == 'isolated':
        # Add the connector and hostname to isolated_connectors
        isolated_connectors[connector_guid] = hostname

# Print the number of connectors found in the first 500 results
print('Connectors found: {}'.format(len(isolated_connectors)))

# Paginate through the rest of the results
while 'next' in response_json['metadata']['links']:
    # Container for storing new connectors
    additional_connectors = {}

    # Name the URL for the next page of results
    next_url = response_json['metadata']['links']['next']

    # Query AMP for Endpoints for the next page of connectors
    response = session.get(next_url)

    # Decode the JSON Response
    response_json = response.json()

    # Name the 'data' list in the JSON response
    data = response_json['data']

    # Iterate over the response data
    for connector in data:
        # Name the elements from the connector that are needed
        isolation = connector.get('isolation', {})
        available = isolation.get('available')
        status = isolation.get('status')
        connector_guid = connector.get('connector_guid')
        hostname = connector.get('hostname')

        # Check if the connector has isolation available and is isolated
        if available and status == 'isolated':
            # Add the connector and hostname to additional_connectors
            additional_connectors[connector_guid] = hostname

    # Print the number of connectors found in this page of 500 results
    print('Connectors found: {}'.format(len(additional_connectors)))

    # Add the connectors from this page to the initial container
    isolated_connectors.update(additional_connectors)

# Print the total number of connectors found
print('Total connectors found that are isolated: {}'.format(
    len(isolated_connectors)))

# Write the GUIDs to a file named 'isolated_connectors.txt'
if isolated_connectors:
    print('\nWriting connector GUIDs to isolated_connectors.txt')
    with open('isolated_connectors.txt', 'w') as file:
        # Iterate over the stored GUIDs
        for guid in isolated_connectors:
            # Write the GUID to the file
            file.write('{}\n'.format(guid))
else:
    print('\nNothing to write to disk')
