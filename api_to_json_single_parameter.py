# will access the API using a single parameter for endpoint
# will save the returned data as json files

from api_to_json_udfs import api_to_json

endpoints = ['timezone', 'countries']
for endpoint in endpoints:
    api_to_json(endpoint)