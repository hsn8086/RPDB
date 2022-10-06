import base64
import json
import os.path
import pickle


class RPDB:
    def __init__(self, path, auto_save=True):
        self.path = path
        if os.path.exists(path):
            self.db_json = json.load(open(self.path, 'r', encoding='utf8'))
        else:
            self.db_json = {}
        self.auto_save = auto_save

    def set(self, key, value):
        if type(value) != str and \
                type(value) != int and \
                type(value) != list and \
                type(value) != dict and \
                type(value) != bool:
            self.db_json[key] = {'DBMark&': 'pickle', 'data': base64.b64encode(pickle.dumps(value)).decode('utf8')}

        else:
            if type(value) == dict:
                if 'DBMark&' in value:
                    raise "Do not write 'DBMark&' to the dict"
            self.db_json[key] = value
        if self.auto_save:
            self.dump()

    def get(self, key):
        if type(self.db_json[key]) == dict:
            if 'DBMark&' in self.db_json[key]:
                if self.db_json[key]['DBMark&'] == 'pickle':
                    return pickle.loads(base64.b64decode(self.db_json[key]['data']))

        return self.db_json[key]

    def exists(self, key):
        return key in self.db_json

    def dump(self):
        json.dump(self.db_json, open(self.path, 'w', encoding='utf8'))

    def getall(self):
        return self.db_json.keys()

    def rem(self, key):
        del self.db_json['key']
        self.dump()
