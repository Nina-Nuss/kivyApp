import json

# Open the file and load its content
with open('db/levels.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for i in data['levels']:
    print(i)