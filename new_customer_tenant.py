
# Snippet Title: New Customer Tenant
# The goal of this script is to enable Census Embedded customers the ability to quickly spin up a new tenant/workspace
# for a customer without having to do a bunch of manual work.  Most Census Embedded customers automate this process with 
# the click of a button because otherwise it creates manual work in the Census UI.

#-----------------------------------------------------------------------------------------------------------------------------------------

# When creating a new tenant for a customer, there are several things that need to be automated:
#   1) Workspace Creation - https://developers.getcensus.com/api-reference/workspaces/create-workspace
#   2) Source Connection - https://developers.getcensus.com/api-reference/sources/create-a-new-source
#   3) Model Creation (optional) - https://developers.getcensus.com/api-reference/models/create-a-new-model
#   4) Adding Users to the tenant (optional) - https://developers.getcensus.com/api-reference/invitations/create-invitation
#      - maybe your support team member or customer success team member

#-----------------------------------------------------------------------------------------------------------------------------------------
import requests, json

# Inputs:
# Org Token or Personal Access Token - In Census UI, navigate to Organization Home > User Settings > New Token.
org_token = '<personal access token>'

# 1) Workspace Creation
# Create new tenant/workspace using the specified Org Token and obtain the newly created Census workspace token, which will
# be used later on.
def create_workspace(org_token):
    url = "https://app.getcensus.com/api/v1/workspaces"
    payload = {
        "name": "<workspace name>",
        "notification_emails": [],
        "return_workspace_api_key": True
    }
    headers = {
        "Authorization": "Bearer " + org_token,
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    response_data = response.json()
    workspace_api_key = response_data['data']['api_key']
    return workspace_api_key

# Run the function & store the workspace API key in variable to be used in later functions.
workspace_api_key = str(create_workspace(org_token))
print("Workspace API Key: " + workspace_api_key)

#-----------------------------------------------------------------------------------------------------------------------------------------

# 2) Source Connection
# Create new Source Connection using source connection details, such as database, schema, port, etc.
# In this example, we are using credential configurations specific to Snowflake.  Note that the payload will likely be configured
# differently based on the source connection type (Snowflake, BigQuery, Redshift, Databricks, etc.).
# See Sources: https://docs.getcensus.com/sources/overview
def create_source(workspace_api_key):
    url = "https://app.getcensus.com/api/v1/sources"

    payload = {"connection": {
            "credentials": {
                "database": "<database>",
                "account": "<account name>",
                "warehouse": "<warehouse name>",
                "password": "<user password>",
                "port": "<port>",
                "user": "<username>"
            },
            "label": "<source connection naming convention>",
            "type": "snowflake"
        }}
    headers = {
        "Authorization": "Bearer " + workspace_api_key,
        "Content-Type": "application/json"
    }

    create_source_response = requests.request("POST", url, json=payload, headers=headers)
    print(create_source_response.text)
    create_source_response_data = create_source_response.json()
    print(create_source_response_data)
    source_id = create_source_response_data['data']['id']
    return source_id

# Run the function and store the newly created source's ID in source_id variable to be used when creating a model
source_id = str(create_source(workspace_api_key))
print("Source ID" + source_id)

#-----------------------------------------------------------------------------------------------------------------------------------------

# 3) Model Creation
# Create a new SQL Model using the workspace token we've generated and the source id that we obtained when creating a new 
# source connection.
def create_model(workspace_token, source_id):
    url = "https://app.getcensus.com/api/v1/sources/" + source_id +"/models"
    payload = {
        "description": "<model description>",
        "name": "<model name>",
        "query": "<sql query>"
    }
    headers = {
        "Authorization": "Bearer " + workspace_token,
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)

# Run the Create Model function to create a new SQL model in the specified tenant/workspace.
create_model(workspace_api_key, source_id)

#-----------------------------------------------------------------------------------------------------------------------------------------

# 4) Add User to the Tenant/Workspace
# Invite a user to be able to access the newly created tenant/workspace. This is common among Census Embedded cusotmers that
# have a support team that needs to be able to troubleshoot from the UI as a backup plan.  You will be able to set RBAC for the
# user using this endpoint.
# RBAC: https://docs.getcensus.com/basics/security-and-privacy/workspaces-and-access-controls
def create_workspace_user(org_token):
    # Fetch newly created workspace ID
    def get_new_workspace_id(org_token):
        url = "https://app.getcensus.com/api/v1/workspaces"
        headers = {"Authorization": "Bearer " + org_token}
        response = requests.request("GET", url, headers=headers)
        response_data = response.json()
        workspace_id = response_data['data'][0]['id']
        return workspace_id
    workspace_id = str(get_new_workspace_id(org_token))
    print('Workspace ID: ' + workspace_id)

    # Invite new user to workspace
    url = "https://app.getcensus.com/api/v1/workspaces/" + workspace_id + "/invitations"

    payload = {
        "emails": ['<user email address>'],
        "role": '<user RBAC role name>'
    }
    headers = {
        "Authorization": "Bearer " + org_token,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    response_data = response.json()
    print(response_data)

create_workspace_user(org_token)

#-----------------------------------------------------------------------------------------------------------------------------------------