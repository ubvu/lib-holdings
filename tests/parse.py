import json


with open('files/test_items.json', 'rb') as f:
    items = json.loads(f.read())['briefRecords']

with open('infile_ocns.csv', 'w') as f:
    for item in items:
        f.write(item['oclcNumber'] + '\n')