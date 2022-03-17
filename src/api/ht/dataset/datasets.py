import os
import json
from flask import jsonify
from .web_services import WServices
from .datasets_jsontable import dataset_jsontable


class DatasetsSearch:

    def __init__(self, advanced_search, is_caching, gql_service):
        self.advanced_search = advanced_search
        self.gql_service = gql_service
        self.is_caching = is_caching
        self.response = ""

    def get_data(self, file_format):
        file_format = file_format.lower()
        valid_formats = ["gff3", "jsontable"]
        if file_format not in valid_formats:
            self.response = 'invalid format: ' + file_format
            return ""
        data = False
        if not self.is_caching:
            data = self.check_cache(file_format)
        if not data:
            try:
                ws = WServices(self.gql_service, self.advanced_search)
                data = ws.get_data()
                if file_format == 'jsontable':
                    data = dataset_jsontable(data)
                    data = json.dumps(data)
                    data = json.loads(data)
                    self.response = jsonify(data)
                else:
                    self.response = {"error": "formato invalido"}
                data = str(data)
                with open("./cache/" + file_format + "_" + self.advanced_search + ".cache", "w") as file:
                    file.write(data)
            except Exception as e:
                print("dataset error: "+str(e))
                self.response = "dataset process error: " + str(e)
        else:
            if file_format == 'jsontable':
                data = json.loads(data)
                self.response = jsonify(data)
            else:
                self.response = {"error": "formato invalido"}

    def check_cache(self, file_format):
        data = False
        if os.path.exists("./cache/" + file_format + "_" + self.advanced_search + ".cache"):
            try:
                return open("./cache/" + file_format + "_" + self.advanced_search + ".cache", "r").read()
            except Exception as e:
                print(e)
        return data
