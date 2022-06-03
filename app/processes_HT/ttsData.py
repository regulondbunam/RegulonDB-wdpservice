import json 


def process_tts_to_jsonGQL(tts):
    jsongql = {'data': tts }
    jsongql = json.dumps( jsongql ) 
    return jsongql

def process_tts_to_jsonT(tts):
    columns = """[
        {"Header": "Start", "accessor": "_start"},
        {"Header": "End", "accessor": "_end"},
        {"Header": "Name", "accessor": "_name"},
        {"Header": "Strand", "accessor": "_strand"},
        {"Header": "ClosestGenes", "accessor": "_gene"}
        ]"""
    data = []
    try:
        for tt in tts:
            genes = "["
            for key in tt:
                if not tt[key]:
                    tt[key] = ""
            try:
                for gen in tt["closestGenes"]:
                    dat = '{"_id":"'+gen['_id']+'","name":"'+gen['name']+'","distanceTo": "'+str(
                        gen['distanceTo'])+'"},'
                    genes = genes + dat
                genes = genes[:-1]
            except:
                print('An exception occurred on tts gene')
            genes = genes + "]"
            if genes is "]":
              genes = []
            data.append(
                f"""{{
                    "_start": "{tt["leftEndPosition"]}",
                    "_end": "{tt["rightEndPosition"]}",
                    "_name": "{tt["name"]}",
                    "_strand": "{tt["strand"]}",
                    "_gene": {genes}
                    }}"""
            )
        data = ",\n".join(data)
    except:
        print('An exception occurred on process_peaks_to_jsonT')
    return f'{{ "columns": {columns}, "data":[{data}] }}'


def process_tts_to_gff3(tts):
    #print(tts[0])
    # NC_000913.3	RegulonDB	transcription_termination_site	308	308	.	+	0	name=TTS_1
    gff3_tts = ""
    for tt in tts:
        for key in tt:
            if not tt[key]:
                tt[key] = ""
        tuple_tt = (
            tt["chromosome"],
            "RegulonDB",
            "transcription_termination_site",
            str(tt["leftEndPosition"]),
            str(tt["rightEndPosition"]),
            ".",
            tt["strand"],
            ".",
            "name="+tt["name"]
        )

        try:
            gff3_tts = gff3_tts+"\t".join(tuple_tt)+"\n"
        except Exception as e:
            print(e)
            print(tt)
    return gff3_tts
