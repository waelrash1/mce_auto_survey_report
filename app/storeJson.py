import json

from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

report_dict = {"id": "10474",
               "filename": "1047.pdf",
               "counter": 1,
               "date": ["E", "F"],
               "uri": ""
               }


with open('jsonReportrecord.txt', 'w') as json_file:
    json.dump(report_dict, json_file)
    print(json.dumps(report_dict, indent=4, sort_keys=True))


@app.route('/record/reports', methods=['POST'])
def create_report_record():
    if not request.json or not 'title' in request.json:
        abort(400)
    report = {
        'id': tasks[-1]['id'] + 1,
        'filename': request.json['folename'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
