import sys, os
from app.utiles import errorRegister


def display_dict(dictionary):
    if dictionary == None:
        return ""
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



def format_txt_gene(gene_data):
    id = ""
    if not gene_data["_id"] == None:
        id = f"""
        id - {gene_data["_id"]}"""
    name = ""
    if not gene_data["gene"]["name"] == None:
        name = f"""
        name - {gene_data["gene"]["name"]}"""
    bnumber = ""
    if not gene_data["gene"]["bnumber"] == None:
        bnumber = f"""
        bnumber - {gene_data["gene"]["bnumber"]}"""
    centisomePosition = ""
    if not gene_data["gene"]["centisomePosition"] == None:
        centisomePosition = f"""
        centisomePosition - {gene_data["gene"]["centisomePosition"]}"""
    gcContent = ""
    if not gene_data["gene"]["gcContent"] == None:
        gcContent = f"""
        gcContent - {gene_data["gene"]["gcContent"]}"""
    leftEndPosition = ""
    if not gene_data["gene"]["leftEndPosition"] == None:
        leftEndPosition = f"""
        leftEndPosition - {gene_data["gene"]["leftEndPosition"]}"""
    rightEndPosition = ""
    if not gene_data["gene"]["rightEndPosition"] == None:
        rightEndPosition = f"""
        rightEndPosition - {gene_data["gene"]["rightEndPosition"]}"""
    strand = ""
    if not gene_data["gene"]["strand"] == None:
        strand = f"""
        strand - {gene_data["gene"]["strand"]}"""
    sequence = ""
    if not gene_data["gene"]["sequence"] == None:
        sequence = f"""
        sequence - {gene_data["gene"]["sequence"]}"""
    note = ""
    if not gene_data["gene"]["note"] == None:
        note = f"""
        note - {gene_data["gene"]["note"]}"""
    externalCrossReferences = ""
    if not gene_data["gene"]["externalCrossReferences"] == None:
        externalCrossReferences = f"""
        {display_array("externalCrossReferences",gene_data["gene"]["externalCrossReferences"],False)}"""   
    products = ""
    if not gene_data["products"] == None:
        products = f"""
        {display_array("products",gene_data["products"],False)}"""
    regulation = ""
    if not gene_data["regulation"] == None:
        statistics = ""
        if not gene_data["regulation"]["statistics"] == None:
            statistics = f"""[{statistics(gene_data["regulation"]["statistics"])}]"""
        operon = ""
        if not gene_data["regulation"]["operon"] == None:
            operon = f"""operon - {gene_data["regulation"]["operon"]["name"]}[{gene_data["regulation"]["operon"]["id"]}]"""
        arrangement = ""
        if not gene_data["regulation"]["operon"]["arrangement"] == None:
            arrangement = f"""{display_array("    arrangement",gene_data["regulation"]["operon"]["arrangement"],True)}"""
        regulation = f"""
        regulation - {statistics}{{
            {operon}
            {arrangement}
            }}"""
    
    try:
        return f"""#RegulonDB txt gene file
{id}{name}{bnumber}{centisomePosition}{gcContent}{leftEndPosition}{rightEndPosition}{strand}{sequence}{note}{externalCrossReferences}{products}{regulation}
    """
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error = f"""on {str(fname)} def format_txt_gene, build txt [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
        errorRegister(error)
        return f"""
Sorry, we seem to have an error in the data mapping.
Please report this problem in the User feedback section:
Error Details:
wdps_ecoli_gene_txt_process - {str(e)}
more Information
{error}
    """
    


"""
fragments - {json.dumps(gene_data["gene"]["fragments"])}
growthConditions - {json.dumps(gene_data["growthConditions"])}
shineDalgarnos - {json.dumps(gene_data["shineDalgarnos"])}
Citations - {json.dumps(gene_data["allCitations"])}
"""
    