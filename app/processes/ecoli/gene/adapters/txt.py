import json


def display_dict(dictionary):
    rel = ""
    for key in dictionary:
        if key != "__typename":
            if type(dictionary[key]) == list:
                rel = rel+display_array("\t"+key,dictionary[key],True)
            elif type(dictionary[key]) == dict:
                rel = rel+display_dict(dictionary[key])
            else:
                rel = rel+"\t"+key+" - "+str(dictionary[key])+"\n"
    return rel

def display_array(name,array,tab = False):
    end = ""
    if tab:
        end = "\t"
    rel = ""
    index = 0
    for element in array:
        if type(element) == dict:
            rel = rel+end+"-["+str(index)+"]-\n"+display_dict(element)
        elif type(element) == list:
            rel = rel+display_array(str(index)+":",element,True)
        else:
            rel = rel+end+"-["+str(index)+"]-\n"+str(element)+"\n"
        index += 1
             
    return f"""{name} - [{len(array)} items] {{
{rel}
{end}}}
"""

def statistics(st):
    rel=""
    for key in st:
        if key != "__typename":
            rel = rel+" "+key+" "+str(st[key])+","
    return rel

def format_txt_gene(gene):
    gene_data = gene["data"][0]
    try:
        return f"""#RegulonDB WDPS txt gene file
id - {gene_data["_id"]}
name - {gene_data["gene"]["name"]}
bnumber - {gene_data["gene"]["bnumber"]}
centisomePosition - {gene_data["gene"]["centisomePosition"]}
gcContent - {gene_data["gene"]["gcContent"]}
leftEndPosition - {gene_data["gene"]["leftEndPosition"]}
rightEndPosition - {gene_data["gene"]["rightEndPosition"]}
strand - {gene_data["gene"]["strand"]}
sequence - {gene_data["gene"]["sequence"]}
note - {gene_data["gene"]["note"]}
{display_array("externalCrossReferences",gene_data["gene"]["externalCrossReferences"],False)}
regulation - [{statistics(gene_data["regulation"]["statistics"])}]{{
    operon - {gene_data["regulation"]["operon"]["name"]}[{gene_data["regulation"]["operon"]["id"]}]
{display_array("    arrangement",gene_data["regulation"]["operon"]["arrangement"],True)}
{display_array("products",gene_data["products"],False)}
}}
    """
    except Exception as e:
        print(e)
        return f"""
Sorry, we seem to have an error in the data mapping.
Please report this problem in the User feedback section:
Error Details:
wdps_ecoli_gene_txt_process - {str(e)}
    """
    


"""
fragments - {json.dumps(gene_data["gene"]["fragments"])}
growthConditions - {json.dumps(gene_data["growthConditions"])}
shineDalgarnos - {json.dumps(gene_data["shineDalgarnos"])}
Citations - {json.dumps(gene_data["allCitations"])}
"""
    