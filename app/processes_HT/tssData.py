import json 


def process_tss_to_jsonGQL(tss):
    jsongql = {'data': tss }
    jsongql = json.dumps( jsongql ) 
    return jsongql


def process_tss_to_jsonT(tss):
    columns = """[
        {"Header": "Start", "accessor": "_start"},
        {"Header": "End", "accessor": "_end"},
        {"Header": "Pos 1", "accessor": "_pos"},
        {"Header": "Strand", "accessor": "_strand"},
        {"Header": "ClosestGenes", "accessor": "_gene"},
        {"Header": "Promoter", "accessor": "_prom"}
        ]"""
    data = []
    try:
        for ts in tss:
            genes = "["
            promoters = "["
            for key in ts:
                if not ts[key]:
                    ts[key] = ""
            try:
                for gen in ts["closestGenes"]:
                    dat = '{"_id":"'+gen['_id']+'","name":"'+gen['name']+'","distanceTo": "'+str(
                        gen['distanceTo'])+'"},'
                    genes = genes + dat
                genes = genes[:-1]
            except:
                print('An exception occurred on tss gene')
            genes = genes + "]"
            if genes is "]":
              genes = []
            try:
                for prom in ts["promoter"]:
                    dat = '{"_id":"'+prom['_id']+'","name":"'+prom['name']+'"},'
                    promoters = promoters + dat
                promoters = promoters[:-1]
            except:
                print('An exception occurred on tss gene')
            promoters = promoters + "]"
            if promoters is "]":
              promoters = []
            data.append(
                f"""{{
                    "_start": "{ts["leftEndPosition"]}",
                    "_end": "{ts["rightEndPosition"]}",
                    "_pos": "{ts["pos_1"]}",
                    "_strand": "{ts["strand"]}",
                    "_gene": {genes},
                    "_prom": {promoters}
                    }}"""
            )
        data = ",\n".join(data)
    except:
        print('An exception occurred on process_peaks_to_jsonT')
    return f'{{ "columns": {columns}, "data":[{data}] }}'


def process_tss_to_gff3(tss):
    # NC_000913.3	RegulonDB	transcription_start_cluster	38	38	.	+	0	name=TSS_1
    #print(tss[0])
    gff3_tss = ""
    for ts in tss:
        for key in ts:
            if not ts[key]:
                ts[key] = ""
        tuple_ts = (
            ts["chromosome"],
            "RegulonDB",
            "transcription_start_cluster",
            str(ts["leftEndPosition"]),
            str(ts["rightEndPosition"]),
            ".",
            ts["strand"],
            ".",
            "name="+ts["_id"]
        )

        try:
            gff3_tss = gff3_tss+"\t".join(tuple_ts)+"\n"
        except Exception as e:
            print(e)
            print(ts)
    return gff3_tss