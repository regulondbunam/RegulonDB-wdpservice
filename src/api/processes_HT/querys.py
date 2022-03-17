class Querys:

    AuthorsDataOfDataset = """
    query AuthorsDataOfDataset($datasetId: String!)
    {
        getAuthorsDataOfDataset(datasetId: $datasetId){
            authorsData
        }
    }
    """

    PeaksDataOfDataset = """
    query PeaksDataOfDataset($datasetId: String!) {
        getAllPeaksOfDataset(datasetId: $datasetId) {
            _id
            name
            closestGenes {
              _id
              name
              distanceTo
              productName
            }
            chromosome
            peakLeftPosition
            peakRightPosition
            score
            siteIds
            datasetIds
            temporalId
        }
    }
    """

    SitesDataOfDataset = """
    query SitesDataOfDataset($datasetId: String!) {
        getAllTFBindingOfDataset(datasetId: $datasetId) {
            _id
            chromosome
            chrLeftPosition
            chrRightPosition
            closestGenes {
                _id
                name
                distanceTo
                transcriptionUnits {
                    _id
                    name
                    distanceTo
                }
            }
            foundClassicRIs {
                tfbsLeftPosition
                tfbsRightPosition
                relativeGeneDistance
                relativeTSSDistance
                strand
                sequence
            }
            foundDatasetRIs {
                tfbsLeftPosition
                tfbsRightPosition
                relativeGeneDistance
                relativeTSSDistance
                strand
                sequence
            }
            peakId
            score
            strand
            sequence
            datasetIds
            temporalId
            nameCollection
        }
    }
    """

    TuDataOfDataset = """
    query TuDataOfDataset($datasetId: String!)
    {
        getAllTransUnitsOfDataset(datasetId: $datasetId){
            _id
            chromosome
            leftEndPosition
            rightEndPosition
            name
            strand
            length
            termType
            genes {
              _id
              name
              bnumber
            }
            phantom
            pseudo
            datasetIds
            temporalId
        }
    }
    """

    TtsOfDataset = """
        query TTSDataOfDataset($datasetId: String!)
        {
            getAllTTSOfDataset(datasetId: $datasetId){
                _id
                chromosome
                leftEndPosition
                rightEndPosition
                name
                strand
                closestGenes {
                  _id
                  name
                  distanceTo
                }
                terminator {
                  _id
                  transcriptionUnits {
                    _id
                    name
                    promoter {
                      _id
                      name
                      sequence
                      leftEndPosition
                      rightEndPosition
                      strand
                    }
                  }
                }
                datasetIds
                temporalId
            }
        }
        """

    TssDataOfDataset = """
        query TSSDataOfDataset($datasetId: String!)
        {
            getAllTSSOfDataset(datasetId: $datasetId){
                _id
                chromosome
                leftEndPosition
                rightEndPosition
                pos_1
                strand
                closestGenes {
                  _id
                  name
                  distanceTo
                }
                promoter {
                  _id
                  name
                  strand
                  pos1
                  sigma
                  confidenceLevel
                }
                datasetIds
            }
        }
        """

    switch_querys = {
        "author": AuthorsDataOfDataset,
        "peaks": PeaksDataOfDataset,
        "sites": SitesDataOfDataset,
        "tus": TuDataOfDataset,
        "tts": TtsOfDataset,
        "tss": TssDataOfDataset
    }
