import json

def format_txt_gene(gene):
    gene_data = gene["data"][0]
    try:
        return f"""#RegulonDB WDPS txt gene file
id - {gene_data["_id"]}
name - {gene_data["gene"]["name"]}
bnumber - {gene_data["gene"]["bnumber"]}
centisomePosition - {gene_data["gene"]["centisomePosition"]}
externalCrossReferences - {json.dumps(gene_data["gene"]["externalCrossReferences"])}
gcContent - {gene_data["gene"]["gcContent"]}
leftEndPosition - {gene_data["gene"]["leftEndPosition"]}
rightEndPosition - {gene_data["gene"]["rightEndPosition"]}
strand - {gene_data["gene"]["strand"]}
sequence - {gene_data["gene"]["sequence"]}
note - {gene_data["gene"]["note"]}
fragments - {json.dumps(gene_data["gene"]["fragments"])}
growthConditions - {json.dumps(gene_data["growthConditions"])}
regulation - {json.dumps(gene_data["regulation"])}
products - {json.dumps(gene_data["products"])}
shineDalgarnos - {json.dumps(gene_data["shineDalgarnos"])}
Citations - {json.dumps(gene_data["allCitations"])}
    """
    except Exception as e:
        print(e)
        return f"""
Sorry, we seem to have an error in the data mapping.
Please report this problem in the User feedback section:
Error Details:
wdps_ecoli_gene_txt_process - {str(e)}
    """
    
    
    