import json

with open("configuration/services_config.json") as f:
    services_data = json.load(f)

print(services_data['kafka']['IP'])
    