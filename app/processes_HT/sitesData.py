import json 


def process_sites_to_jsonGQL(sites):
    jsongql = {'data': sites }
    jsongql = json.dumps( jsongql ) 
    return jsongql


def process_sites_to_jsonT(sites):
    columns = """[
        {"Header": "Start", "accessor": "_start"},
        {"Header": "End", "accessor": "_end"},
        {"Header": "Score", "accessor": "_score"},
        {"Header": "Strand", "accessor": "_strand"},
        {"Header": "Sequence", "accessor": "_sequence"},
        {"Header": "ClosestGenes", "accessor": "_gene"}
        ]"""
    data = []
    try:
        for site in sites:
            genes = "["
            for key in site:
                if not site[key]:
                    site[key] = ""
            try:
                for gen in site["closestGenes"]:
                    tus = []
                    for tu in gen["transcriptionUnits"]:
                        tus.append(tu["name"])
                    dat = '{"_id":"'+gen['_id']+'","name":"'+gen['name']+'","distanceTo": "'+str(
                        gen['distanceTo'])+'", "transcriptionUnits": "'+', '.join(tus)+'"},'
                    genes = genes + dat
                genes = genes[:-1]
                genes = genes + "]"
            except:
                genes="[]"
                print('An exception occurred on site')
            if genes is "]":
              genes = []
            data.append(
                f"""{{
                    "_start": "{site["chrLeftPosition"]}",
                    "_end": "{site["chrRightPosition"]}",
                    "_score": "{site["score"]}",
                    "_strand": "{site["strand"]}",
                    "_sequence": "{site["sequence"]}",
                    "_gene": {genes}
                    }}"""
            )
        data = ",\n".join(data)
    except:
        print('An exception occurred on process_peaks_to_jsonT')
    return f'{{ "columns": {columns}, "data":[{data}] }}'


def process_sites_to_gff3(sites):
    #print(sites)
    # chromosome,RegulonDB,binding_site,chrLeftPosition,chrRightPosition,score,strand,.,name="";sequence=CGAT
    gff3_sites = ""
    for site in sites:
        for key in site:
            if not site[key]:
                site[key] = ""
        tuple_site = (
            site["chromosome"],
            "RegulonDB",
            "binding_site",
            str(site["chrLeftPosition"]),
            str(site["chrRightPosition"]),
            str(site["score"]),
            site["strand"],
            ".",
            "name="+site["_id"]+";sequence="+site["sequence"]
        )
        try:
            gff3_sites = gff3_sites+"\t".join(tuple_site)+"\n"
        except Exception as e:
            print(e)
            print(site)
    return gff3_sites
