from .introspection import Dataset

COLUMNS = [
    {"Header": "_id", "accessor": "_id"},
    {"Header": "referenceGenome", "accessor": "referenceGenome"},
    {"Header": "datasetType", "accessor": "datasetType"},
    {"Header": "Transcription Factor", "accessor": "objectsTested_name"},
    {"Header": "Dataset Title", "accessor": "sample_title"},
    {"Header": "publications", "accessor": "publications_title"},
    {"Header": "authors", "accessor": "publications_authors"},
    {"Header": "sourceSerie", "columns": [
        {"Header": "title", "accessor": "sourceSerie_title"},
        {"Header": "strategy", "accessor": "sourceSerie_strategy"},
        {"Header": "method", "accessor": "sourceSerie_method"}
    ]},
    {"Header": "growthConditions", "columns": [
        {"Header": "organism", "accessor": "growthConditions_organism"},
        {"Header": "geneticBackground", "accessor": "growthConditions_geneticBackground"},
        {"Header": "medium", "accessor": "growthConditions_medium"},
        {"Header": "aeration", "accessor": "growthConditions_aeration"},
        {"Header": "temperature", "accessor": "growthConditions_temperature"},
        {"Header": "ph", "accessor": "growthConditions_ph"},
        {"Header": "pressure", "accessor": "growthConditions_pressure"},
        {"Header": "opticalDensity", "accessor": "growthConditions_opticalDensity"},
        {"Header": "growthPhase", "accessor": "growthConditions_growthPhase"},
        {"Header": "growthRate", "accessor": "growthConditions_growthRate"},
        {"Header": "vesselType", "accessor": "growthConditions_vesselType"},
        {"Header": "aerationSpeed", "accessor": "growthConditions_aerationSpeed"},
        {"Header": "mediumSupplements", "accessor": "growthConditions_mediumSupplements"},
    ]}
]


def dataset_jsontable(datasets):
    # Make Columns!
    columns = COLUMNS
    data = []
    for dataset in datasets:
        try:
            sample_title = ""
            sourceSerie_title = ""
            sourceSerie_strategy = ""
            sourceSerie_method = ""
            publications = ""
            authors = ""
            tfs = ""
            growthConditions_organism = ""
            growthConditions_geneticBackground = ""
            growthConditions_medium = ""
            growthConditions_aeration = ""
            growthConditions_temperature = ""
            growthConditions_ph = ""
            growthConditions_pressure = ""
            growthConditions_opticalDensity = ""
            growthConditions_growthPhase = ""
            growthConditions_growthRate = ""
            growthConditions_vesselType = ""
            growthConditions_aerationSpeed = ""
            growthConditions_mediumSupplements = ""
            try:
                for publication in dataset['publications']:
                    publications = publications + " " + publication['title']
                    authors = authors + " " + str(publication['authors'])
            except Exception as e:
                print(e)
            try:
                for tf in dataset["objectsTested"]:
                    tfs = tfs + " " + tf["name"]
            except Exception as e:
                print(e)
            if dataset["growthConditions"]:
                growthConditions_organism = str(dataset["growthConditions"]["organism"])
                growthConditions_geneticBackground = dataset["growthConditions"]["geneticBackground"]
                growthConditions_medium = dataset["growthConditions"]["medium"]
                growthConditions_aeration = dataset["growthConditions"]["aeration"]
                growthConditions_temperature = dataset["growthConditions"]["temperature"]
                growthConditions_ph = dataset["growthConditions"]["ph"]
                growthConditions_pressure = dataset["growthConditions"]["pressure"]
                growthConditions_opticalDensity = dataset["growthConditions"]["opticalDensity"]
                growthConditions_growthPhase = dataset["growthConditions"]["growthPhase"]
                growthConditions_growthRate = dataset["growthConditions"]["growthRate"]
                growthConditions_vesselType = dataset["growthConditions"]["vesselType"]
                growthConditions_aerationSpeed = dataset["growthConditions"]["aerationSpeed"]
                growthConditions_mediumSupplements = dataset["growthConditions"]["mediumSupplements"]
            if dataset["sample"]:
                sample_title = dataset['sample']['title']
            if dataset["sourceSerie"]:
                sourceSerie_title = dataset["sourceSerie"]["title"]
                sourceSerie_strategy = dataset["sourceSerie"]["strategy"]
                sourceSerie_method = dataset["sourceSerie"]["method"]
            row = {
                "_id": dataset["_id"],
                "sample_title": sample_title,
                "referenceGenome": dataset["referenceGenome"],
                "datasetType": dataset["datasetType"],
                "publications_title": publications,
                "publications_authors": authors,
                "objectsTested_name": tfs,
                "sourceSerie_title": sourceSerie_title,
                "sourceSerie_strategy": sourceSerie_strategy,
                "sourceSerie_method": sourceSerie_method,
                "growthConditions_organism": growthConditions_organism,
                "growthConditions_geneticBackground": growthConditions_geneticBackground,
                "growthConditions_medium": growthConditions_medium,
                "growthConditions_aeration": growthConditions_aeration,
                "growthConditions_temperature": growthConditions_temperature,
                "growthConditions_ph": growthConditions_ph,
                "growthConditions_pressure": growthConditions_pressure,
                "growthConditions_opticalDensity": growthConditions_opticalDensity,
                "growthConditions_growthPhase": growthConditions_growthPhase,
                "growthConditions_growthRate": growthConditions_growthRate,
                "growthConditions_vesselType": growthConditions_vesselType,
                "growthConditions_aerationSpeed": growthConditions_aerationSpeed,
                "growthConditions_mediumSupplements": growthConditions_mediumSupplements
            }
            data.append(row)
        except Exception as e:
            print("error", e)
            print(dataset["_id"])
    return {
        "columns": columns,
        "data": data,
    }