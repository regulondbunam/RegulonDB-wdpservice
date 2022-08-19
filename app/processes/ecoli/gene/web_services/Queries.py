class Queries:

    GET_GENE_BY_SEARCH = """
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
    """
