
totalOf = {
    "inDataset": int,
    "inRDBClassic": int,
    "sharedItems": int,
    "notInRDB": int,
    "notInDataset": int
}

DatasetSummary = {
    "totalOfPeaks": totalOf,
    "totalOfGenes": totalOf,
    "totalOfTFBS": totalOf,
}

ReleaseDataControl = {
    "date": str,
    "version": str
}

HTGrowthCondition = {
    "organism": str,
    "geneticBackground": str,
    "medium": str,
    "aeration": str,
    "temperature": str,
    "ph": str,
    "pressure": str,
    "opticalDensity": str,
    "growthPhase": str,
    "growthRate": str,
    "vesselType": str,
    "aerationSpeed": str,
    "mediumSupplements": str,
    "otherTerms": str
}

LinkedDataset = {
    "controlId": str,
    "experimentId": str,
    "datasetType": str
}

DatasetSample = {
    "experimentId": str,
    "controlId": str,
    "title": str,
    "srrId": str
}

Platform = {
    "_id": str,
    "source": str,
    "title": str
}

Serie = {
    "sourceId": str,
    "sourceName": str
}

SourceSerie = {
    "series": [Serie],
    "platform": Platform,
    "title": str,
    "strategy": str,
    "method": str,
    "readType": str
}

objectTestedGene = {
    "_id": str,
    "name": str
}

ExternalCrossReferences = {
    "externalCrossReferenceId": str,
    "externalCrossReferenceName": str,
    "objectId": str,
    "url": str
}

ObjectTested = {
    "name": str,
    "synonyms": str,
    "genes_name": str,
    "note": str,
    "activeConformations": str,
}

DatasetPublication = {
    "pmid": int,
    "doi": str,
    "authors": str,
    "title": str,
    "date": str,
    "pmcid": str,
    "abstract": str,
}

Dataset = {
    "_id": str,
    "referenceGenome": str,
    "datasetType": str,
    "temporalId": str,
    "publications": [DatasetPublication],
    "objectsTested": [ObjectTested],
    "sourceSerie": SourceSerie,
    "sample": DatasetSample,
    "linkedDataset": LinkedDataset,
    "growthConditions": HTGrowthCondition,
    "releaseDataControl": ReleaseDataControl,
    "summary": DatasetSummary,
    "assemblyGenomeId": str,
    "fivePrimeEnrichment": str,
    "nlpGrowthConditionsId": str,
    "geneExpressionFiltered": str,
    "experimentCondition": str,
}
