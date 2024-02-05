
# Snippet Title: Create New Sync
# The goal of this script is to enable Census Embedded customers the ability to quickly create a new sync programmatically using the 
# existing source & destination connects in a specific client's workspaces. Most Census Embedded customers automate this process with 
# the click of a button because otherwise it creates manual work in the Census UI.

#-----------------------------------------------------------------------------------------------------------------------------------------

# When creating a new tenant for a customer, there are several things that need to be automated:
#   1) Get Source ID in Workspace - https://developers.getcensus.com/api-reference/sources/list-sources
#   2) Get Model Name in Workspace - https://developers.getcensus.com/api-reference/models/list-models
#   3) Get Destination ID in Workspace - https://developers.getcensus.com/api-reference/destinations/list-destinations
#   4) Create Sync - https://developers.getcensus.com/api-reference/syncs/create-a-new-sync 

#-----------------------------------------------------------------------------------------------------------------------------------------

import requests, json

# Inputs:
# 1) Org Token or Personal Access Token - In Census UI, navigate to Organization Home > User Settings > New Token.
# 2) Workspace API Key - In Census UI, navigate to workspace settings
#     - or fetch workspace API key using API - https://developers.getcensus.com/api-reference/workspaces/list-workspaces

org_token = '<personal access token>'
workspace_api_key = '<workspace token>'

#-----------------------------------------------------------------------------------------------------------------------------------------

# 1) Get Source ID in Workspace
# Using the API, GET the Source ID of the connected Source within the Workspace.  This will end up getting used when configuring a
# sync later on.

def grab_source_id(workspace_api_key):
    url = "https://app.getcensus.com/api/v1/sources"
    headers = {
        "Authorization": "Bearer " + workspace_api_key
    }
    response = requests.request("GET", url, headers=headers)
    response_data = response.json()
    source_id = response_data['data'][0]['id']
    return source_id

source_id = str(grab_source_id(workspace_api_key))
print("Source ID: " + source_id)

#-----------------------------------------------------------------------------------------------------------------------------------------

# 2) Get Model Name in Workspace
# Using the API, GET the Model Name of the connected Model within the Workspace.  This will end up getting used when configuring a
# sync later on.

def grab_model_name(workspace_api_key, source_id):
    url = "https://app.getcensus.com/api/v1/sources/" + source_id + "/models"

    headers = {
        "Authorization": "Bearer " + workspace_api_key
    }

    response = requests.request("GET", url, headers=headers)
    response_data = response.json()
    model_name = response_data['data'][0]['name']
    return model_name

model_name = grab_model_name(workspace_api_key, source_id)
print("Model Name: " + model_name)
#-----------------------------------------------------------------------------------------------------------------------------------------

# 3) Get Destination ID in Workspace
# Using the API, GET the Destination ID of the connected Destination within the Workspace.  This will end up getting used when configuring a
# sync later on.

def grab_destination_id(workspace_api_key):
    url = "https://app.getcensus.com/api/v1/destinations"
    headers = {
        "Authorization": "Bearer " + workspace_api_key
    }
    response = requests.request("GET", url, headers=headers)
    response_data = response.json()
    destination_id = response_data['data'][0]['id']
    return destination_id

destination_id = str(grab_destination_id(workspace_api_key))
print("Destination ID: " + destination_id)

#-----------------------------------------------------------------------------------------------------------------------------------------

# 4) Create Sync
# Using the Source ID, Destination ID, and the Model Name - create a new sync!
# There are a lot of inputs when configuring a new Sync that need to be manually set or fetched from elsewhere.  To ensure that sync
# creation is programmatic and/or automated, you can fetch mapping values and source attribute values using the Census API.  This is
# not currently set up in this example, however these are the two endpoints you would use if you wanted to further automate this process:
#   - Fetch Destination Objects: https://developers.getcensus.com/api-reference/destinations/list-destination-objects
#   - Fetch Model Columns: https://developers.getcensus.com/api-reference/models/fetch-model 

url = "https://app.getcensus.com/api/v1/syncs"
payload = {
    "cron_expression": "* 1 * * *",
    "destination_attributes": {
        "connection_id": destination_id,
        "object": "contact"
    },
    "label": "Census Quick Start Sample Sync",
    "mappings": [
        {
            "from": {
                "data": "EMAIL",
                "type": "column"
            },
            "is_primary_identifier": True,
            "to": "email"
        }
    ],
    "operation": "upsert",
    "paused": False,
    "source_attributes": {
        "connection_id": source_id,
        "object": {

            # automate grabbing model
            "name": model_name,
            "type": "model"
        }
    },
    "triggers": {
        "dbt_cloud": {},
        "fivetran": {},
        "sync_sequence": {}
    }
}
headers = {
    "Authorization": "Bearer " + workspace_api_key,
    "Content-Type": "application/json"
}
response = requests.request("POST", url, json=payload, headers=headers)
response_data = response.json()
print(response.text)

#-----------------------------------------------------------------------------------------------------------------------------------------