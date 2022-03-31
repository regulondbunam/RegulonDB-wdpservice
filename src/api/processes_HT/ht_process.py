import os
import json
from flask import Response, jsonify
from .querys import Querys
from .web_services import WServices
from .authorData import formatData_to_json_author_table
from .sitesData import process_sites_to_gff3
from .peaksData import process_peaks_to_gff3
from .tuData import process_tus_to_gff3
from .ttsData import process_tts_to_gff3
from .tssData import process_tss_to_gff3
from .geneExpression import process_ge_to_bedgraph, process_ge_to_jsont


class HTprocess:
    querys = Querys()

    def __init__(self, dataset_id, gql_service):
        self.dataset_id = dataset_id
        self.gql_service = gql_service
        self.ht_response = ""

    def get_data(self, file_format, data_type):
        file_format = file_format.lower()
        valid_formats = ["gff3", "jsontable", "bedgraph"]
        if file_format not in valid_formats:
            self.ht_response = 'invalid format: ' + file_format
            return ""
        data = self.check_cache(file_format, data_type)
        if not data:
            try:
                ws = WServices(self.gql_service, self.dataset_id, data_type)
                data = ws.get_data()
                if file_format == 'gff3':
                    if data_type == "sites":
                        data = process_sites_to_gff3(data)
                    elif data_type == "peaks":
                        data = process_peaks_to_gff3(data)
                    elif data_type == "tus":
                        data = process_tus_to_gff3(data)
                    elif data_type == "tts":
                        data = process_tts_to_gff3(data)
                    elif data_type == "tss":
                        data = process_tss_to_gff3(data)
                    else:
                        data = "error : file format ht process"
                    self.ht_response = Response(
                        data,
                        mimetype="text/gff3",
                        headers={"Content-disposition": "attachment; gff3_"+data_type+"_" + self.dataset_id + ".gff3"}
                    )
                elif file_format == "bedgraph":
                    if data_type == "ge":
                        data = process_ge_to_bedgraph(data)
                    else:
                        data = "error : file format ht process"
                    self.ht_response = Response(
                        data,
                        mimetype="text/bedgraph",
                        headers={
                            "Content-disposition": "attachment; bedgraph_" + data_type + "_" + self.dataset_id + ".bedgraph"}
                    )
                elif file_format == "jsontable":
                    if data_type == "ge":
                        data = process_ge_to_jsont(data)
                    else:
                        data = "{error : file format ht process}"
                    data_json = json.loads(data)
                    self.ht_response = jsonify(data_json)
                else:
                    data = str(data)
                with open("./cache/" + self.dataset_id + "_"+data_type+"_" + file_format + ".cache", "w") as file:
                    file.write(data)
            except Exception as e:
                print(e)
                self.ht_response = "51 ht process Error: " + str(e)
        else:
            if file_format == 'gff3':
                self.ht_response = Response(
                    data,
                    mimetype="text/gff3",
                    headers={"Content-disposition": "attachment; gff3_sites_" + self.dataset_id + ".gff3"}
                )
            elif file_format == "bedgraph":
                self.ht_response = Response(
                    data,
                    mimetype="text/bedgraph",
                    headers={
                        "Content-disposition": "attachment; bedgraph_" + data_type + "_" + self.dataset_id + ".bedgraph"}
                )
            elif file_format == "jsontable":
                data = json.loads(data)
                self.ht_response = jsonify(data)
            else:
                self.ht_response = 'invalid format: ' + file_format

    def author_data(self, file_format):
        file_format = file_format.lower()
        valid_formats = ["cvs", "jsontable"]
        if file_format not in valid_formats:
            self.ht_response = 'invalid format: ' + file_format
            return ""
        query = self.querys.AuthorsDataOfDataset
        variables = {"datasetId": "" + self.dataset_id}
        data = self.check_cache(file_format, "author")
        if not data:
            data = self.gql_service(query, variables)
            try:
                # print("consulta")
                data = data['data']['getAuthorsDataOfDataset'][0]['authorsData']
                if file_format == 'jsontable':
                    data = json.dumps(formatData_to_json_author_table(data))
                with open("./cache/" + self.dataset_id + "_author_" + file_format + ".cache", "w") as file:
                    file.write(data)
            except Exception as e:
                print(e)
                data = "error: " + str(e)
        # print("cache")
        if file_format == 'cvs':
            self.ht_response = Response(
                data,
                mimetype="text/csv",
                headers={"Content-disposition": "attachment; authorData_author_" + self.dataset_id + ".csv"}
            )
        elif file_format == 'jsontable':
            # print(data)
            data = json.loads(data)
            self.ht_response = jsonify(data)
        else:
            self.ht_response = 'invalid format: ' + file_format

    def check_cache(self, file_format, data_type):
        data = False
        if os.path.exists("./cache/" + self.dataset_id + "_" + file_format + "_" + data_type + ".cache"):
            try:
                return open("./cache/" + self.dataset_id + "_" + file_format + "_" + data_type + ".cache", "r").read()
            except Exception as e:
                print(e)
        return data

    def get_response(self):
        return self.ht_response
