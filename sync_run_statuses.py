# Snippet Title: Print & Return Sync Run Information
# The goal of this script is to enable Census Embedded customers the ability to quickly implement some logic that prints & returns
# information about recent sync runs.  This can be easily changed to target sync runs that have failed or are in progress.  Ultimately,
# Census Embedded customers like to surface sync details to their clients in their own product - this is a great starting point for
# implementing this into an application.

#-----------------------------------------------------------------------------------------------------------------------------------------

import requests, json

workspace_api_key = "<workspace token>"


# Grab all sync IDs within a given workspace and place them into an array.
# Using this endpoint: https://developers.getcensus.com/api-reference/syncs/list-syncs
url = "https://app.getcensus.com/api/v1/syncs"
headers = {"Authorization": "Bearer " + workspace_api_key}
response = requests.request("GET", url, headers=headers)
response_data = response.json()
sync_data = response_data['data']
i = 0
sync_id_array = []
while i < len(sync_data):
    sync_id = str(sync_data[i]['id'])
    sync_id_array.append(sync_id)
    i=i+1
l = 0
print("-----------------------------------------------------")

# For each sync ID, get all sync run data from each sync.
# Using this endpoint: https://developers.getcensus.com/api-reference/sync-runs/list-sync-runs
while l < len(sync_id_array):
    local_sync_id = sync_id_array[l]
    url = "https://app.getcensus.com/api/v1/syncs/" + local_sync_id + "/sync_runs"
    headers = {"Authorization": "Bearer " + workspace_api_key}
    response = requests.request("GET", url, headers=headers)
    sync_run_response_data = response.json()
    sync_run_data = sync_run_response_data['data']

    # For each Sync Run, we want to do something based on the status of the sync.
    # For example, if the sync run status is marked as 'completed', we want to print key information
    # about that sync.  In this example, we print: Sync Run ID, Sync Status, # of Records updated.
    # This can be altered to print whatever you need to from the API response. See this endpoint to understand
    # what other information can be printed: https://developers.getcensus.com/api-reference/sync-runs/list-sync-runs
    k = 0
    while k < len(sync_run_data):
        local_sync_run = sync_run_data[k]
        if local_sync_run['status'] == 'completed':
            print("Sync Run ID: " + str(local_sync_run['id']))
            print("Sync Status: " + local_sync_run['status'])
            print("Records Updated: " + str(local_sync_run['records_updated']))
            print("-----------------------------------------------------")
        else:
            print("Sync ID " + str(local_sync_run['id']) + " has failed!")
            print("-----------------------------------------------------")
        k = k + 1
    l = l + 1


