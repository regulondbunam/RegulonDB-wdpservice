class Queries:

    fragment_CITATIONS = '''
    fragment CITATIONS on Citations {
      publication {
        id
        authors
        pmid
        citation
        url
        title
        year
        __typename
      }
      evidence {
        id
        name
        code
        type
        __typename
      }
      __typename
    }
    '''

    fragment_PAGINATION = '''
    fragment PAGINATION on Pagination {
      currentPage
      firstPage
      hasNextPage
      lastPage
      limit
      totalResults
      __typename
    }
    '''

    fragment_ExternalCrossReferences = '''
    fragment ExternalCrossReferences on ExternalCrossReferences {
      externalCrossReferenceId
      externalCrossReferenceName
      objectId
      url
    }
    '''

    fragments_PRODUCTS = '''
    fragment PRODUCTS on Products {
      anticodon
      cellularLocations
      citations {
        ...CITATIONS
        __typename
      }
      externalCrossReferences {
        ...ExternalCrossReferences
        __typename
      }
      geneOntologyTerms {
        biologicalProcess {
          citations {
            ...CITATIONS
            __typename
          }
          id
          name
          productsIds
          __typename
        }
        cellularComponent {
          citations {
            ...CITATIONS
            __typename
          }
          id
          name
          productsIds
          __typename
        }
        molecularFunction {
          citations {
            ...CITATIONS
            __typename
          }
          id
          name
          productsIds
          __typename
        }
        __typename
      }
      id
      isRegulator
      isoelectricPoint
      molecularWeight
      motifs {
        description
        id
        dataSource
        leftEndPosition
        note
        rightEndPosition
        sequence
        type
        __typename
      }
      name
      note
      regulonId
      sequence
      synonyms
      type
      __typename
    }
    '''

    fragment_PROMOTERS = '''
  fragment PROMOTER on Promoter {
  bindsSigmaFactor {
    citations {
      ...CITATIONS
      __typename
    }
    sigmaFactor_id
    sigmaFactor_name
    __typename
  }
  boxes {
    leftEndPosition
    rightEndPosition
    sequence
    type
    __typename
  }
  citations {
    ...CITATIONS
    __typename
  }
  id
  name
  note
  regulatorBindingSites {
    function
    regulator {
      _id
      function
      name
      __typename
    }
    regulatoryInteractions {
      _id
      centerPosition
      citations {
        ...CITATIONS
        __typename
      }
      function
      mechanism
      note
      regulatorySite {
        _id
        absolutePosition
        citations {
          ...CITATIONS
          __typename
        }
        leftEndPosition
        length
        note
        rightEndPosition
        sequence
        __typename
      }
      __typename
    }
    __typename
  }
  score
  sequence
  synonyms
  transcriptionStartSite {
    leftEndPosition
    range
    rightEndPosition
    type
    __typename
  }
  __typename
}
  '''

    fragment_REGULATION = '''
  fragment REGULATION on Regulation {
  operon {
    arrangement {
      promoters {
        ...PROMOTER
        __typename
      }
      regulator {
        function
        id
        name
        type
        __typename
      }
      transcriptionUnit {
        id
        name
        __typename
      }
      __typename
    }
    id
    name
    __typename
  }
  regulators {
    function
    id
    name
    type
    __typename
  }
  statistics {
    promoters
    regulators
    regulatoryInteractions
    __typename
  }
  __typename
}
  '''

    fragment_GENE = '''
  fragment GENE on Gene {
  bnumber
  centisomePosition
  citations {
    ...CITATIONS
    __typename
  }
  externalCrossReferences {
    ...ExternalCrossReferences
    __typename
  }
  fragments {
    centisomePosition
    id
    leftEndPosition
    name
    rightEndPosition
    sequence
    __typename
  }
  gcContent
  id
  leftEndPosition
  multifunTerms {
    id
    label
    name
    __typename
  }
  name
  note
  rightEndPosition
  sequence
  strand
  synonyms
  type
  __typename
}
  '''

    fragment_SHINE = '''
  fragment SHINEDALGARNOS on ShineDalgarnos {
  distanceToGene
  id
  leftEndPosition
  note
  rightEndPosition
  sequence
  __typename
}
  '''

    fragment_GC = '''
  fragment GROWTHCONDITIONS on GrowthConditions {
  citations {
    ...CITATIONS
    __typename
  }
  controlCondition
  effect
  experimentalCondition
  id
  __typename
}
  '''

    GET_GENE_BY_ID = f"""
    {fragment_CITATIONS}
    {fragment_PAGINATION}
    {fragment_ExternalCrossReferences}
    {fragments_PRODUCTS}
    {fragment_PROMOTERS}
    {fragment_REGULATION}
    {fragment_GENE}
    {fragment_SHINE}
    {fragment_GC}
  query GetGeneInfo($advancedSearch: String, $fullMatchOnly: Boolean = false, $limit: Int = 10, $organismName: String, $page: Int = 0, $properties: [String] = ["gene.id", "gene.name", "gene.synonyms", "gene.type", "products.name"], $search: String) {{
  getGenesBy(advancedSearch: $advancedSearch, fullMatchOnly: $fullMatchOnly, limit: $limit, organismName: $organismName, page: $page, properties: $properties, search: $search) {{
    data {{
      _id
      schemaVersion
      organism {{
        id
        name
        __typename
      }}
      allCitations {{
        ...CITATIONS
        __typename
      }}
      gene {{
        ...GENE
        __typename
      }}
      shineDalgarnos {{
        ...SHINEDALGARNOS
        __typename
      }}
      growthConditions {{
        ...GROWTHCONDITIONS
        __typename
      }}
      products {{
        ...PRODUCTS
        __typename
      }}
      regulation {{
        ...REGULATION
        __typename
      }}
      __typename
    }}
    pagination {{
      ...PAGINATION
      __typename
    }}
    __typename
  }}
}}
  """

    GET_ALL_GENES = '''
  {
    getAllGenes(limit: 0){
      data {
        _id
        gene {
          name
          leftEndPosition
          rightEndPosition
          strand
          synonyms
        }
        products {
          name
        }
      }
    }
  }
  '''

    GET_GENE_BY_SEARCH = '''
    query GET_GENE_BY_SEARCH($search: String, $limit: Int = 10, $page: Int = 0) {
      getGenesBy(search: $search, limit: $limit, page: $page) {
        data {
          _id
          gene {
            name
            leftEndPosition
            rightEndPosition
            strand
            synonyms
          }
          products {
            name
          }
        }
        pagination {
          currentPage
          firstPage
          hasNextPage
          lastPage
          limit
          totalResults
        }
      }
    }
  '''
