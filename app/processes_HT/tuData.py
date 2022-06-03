import json 


def process_tus_to_jsonGQL(tus):
    jsongql = {'data': tus }
    jsongql = json.dumps( jsongql ) 
    return jsongql


def process_tus_to_jsonT(tus):
    columns = """[
        {"Header": "Start", "accessor": "_start"},
        {"Header": "End", "accessor": "_end"},
        {"Header": "Name", "accessor": "_name"},
        {"Header": "Strand", "accessor": "_strand"},
        {"Header": "Genes", "accessor": "_gene"}
        ]"""
    data = []
    try:
        for tu in tus:
            genes = "["
            for key in tu:
                if not tu[key]:
                    tu[key] = ""
            try:
                for gen in tu["genes"]:
                    dat = '{"_id":"'+gen['_id']+'","name":"'+gen['name']+'"},'
                    genes = genes + dat
                genes = genes[:-1]
            except:
                print('An exception occurred on tus gene')
            genes = genes + "]"
            if genes is "]":
              genes = []
            data.append(
                f"""{{
                    "_start": "{tu["leftEndPosition"]}",
                    "_end": "{tu["rightEndPosition"]}",
                    "_name": "{tu["name"]}",
                    "_strand": "{tu["strand"]}",
                    "_gene": {genes}
                    }}"""
            )
        data = ",\n".join(data)
    except:
        print('An exception occurred on process_peaks_to_jsonT')
    return f'{{ "columns": {columns}, "data":[{data}] }}'


def process_tus_to_gff3(tus):
    print(tus[0])
    # chromosome,RegulonDB,transcript_region,chrLeftPosition,chrRightPosition,score,strand,.,name=TU_1;TUlength=162;TUgenes=b0001
    gff3_tus = ""
    for tu in tus:
        genes = []
        for gen in tu["genes"]:
            genes.append(gen["bnumber"])
        if ",".join(genes):
            genes = ",".join(genes)
        else:
            genes = "."
        for key in tu:
            if not tu[key]:
                tu[key] = ""
        tuple_tu = (
            tu["chromosome"],
            "RegulonDB",
            "transcript_region",
            str(tu["leftEndPosition"]),
            str(tu["rightEndPosition"]),
            ".",
            tu["strand"],
            ".",
            "name="+tu["name"]+";TUlength="+str(tu["length"])+";TUgenes="+genes
        )

        try:
            gff3_tus = gff3_tus+"\t".join(tuple_tu)+"\n"
        except Exception as e:
            print(e)
            print(tu)
    return gff3_tus
