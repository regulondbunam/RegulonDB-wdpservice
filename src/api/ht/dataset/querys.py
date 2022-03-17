class Querys:

    getDatasets = """
        query AuthorsDataOfDataset($advancedSearch: String!) {
  getDatasetsFromSearch(advancedSearch: $advancedSearch) {
    _id
    publications {
      pmid
      doi
      authors
      title
      date
      pmcid
    }
    fivePrimeEnrichment
    objectsTested {
      name
      synonyms
      genes {
        name
      }
      note
      activeConformations
    }
    sourceSerie{
      series {
        sourceId
        sourceName
      }
      platform {
        _id
        source
        title
      }
      title
      strategy
      method
    }
    sample {
      experimentId
      controlId
      title
    }
    linkedDataset {
      controlId
      experimentId
      datasetType
    }
    referenceGenome
    datasetType
    temporalId
    growthConditions {
      organism
      geneticBackground
      medium
      mediumSupplements
      aeration
      temperature
      ph
      pressure
      opticalDensity
      growthPhase
      growthRate
      vesselType
      aerationSpeed
    }
    releaseDataControl {
      date
      version
    }
  }
}
        """