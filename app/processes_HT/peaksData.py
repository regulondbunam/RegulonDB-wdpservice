import json 


def process_peaks_to_jsonGQL(peaks):
    jsongql = {'data': peaks }
    jsongql = json.dumps( jsongql ) 
    return jsongql


def process_peaks_to_jsonT(peaks):
    columns = """[
        {"Header": "Start", "accessor": "_start"},
        {"Header": "End", "accessor": "_end"},
        {"Header": "Score", "accessor": "_score"},
        {"Header": "Peak", "accessor": "_name"},
        {"Header": "ClosestGenes", "accessor": "_gene"}
        ]"""
    data = []
    try:
        for peak in peaks:
            genes = "["
            for key in peak:
                if not peak[key]:
                    peak[key] = ""
            try:
                for gen in peak["closestGenes"]:
                    products = ", ".join(gen["productName"])
                    dat = '{"_id":"'+gen['_id']+'","name":"'+gen['name']+'","distanceTo": "'+str(
                        gen['distanceTo'])+'", "productName": "'+products+'"},'
                    genes = genes + dat
                genes = genes[:-1]
            except:
                print('An exception occurred on peak')
            genes = genes + "]"
            if genes is "]":
              genes = []
            data.append(
                f"""{{
                    "_start": "{peak["peakLeftPosition"]}",
                    "_end": "{peak["peakRightPosition"]}",
                    "_score": "{peak["score"]}",
                    "_name": "{peak["name"]}",
                    "_gene": {genes}
                    }}"""
            )
        data = ",\n".join(data)
    except:
        print('An exception occurred on process_peaks_to_jsonT')
    return f'{{ "columns": {columns}, "data":[{data}] }}'


def process_peaks_to_gff3(peaks):
    #print(peaks)
    # NC_000913.3	RegulonDB	ChIP_seq_region	120	515	193	.	.
    # name=peak_1;FC_summitlog10=1.70158;pval_summitlog10=22.0292;qval_summit=19.3913;relative_summit_pos=81
    gff3_peaks = ""
    for peak in peaks:
        for key in peak:
            if not peak[key]:
                peak[key] = ""
        tuple_site = (
            peak["chromosome"],
            "RegulonDB",
            "ChIP_seq_region",
            str(peak["peakLeftPosition"]),
            str(peak["peakRightPosition"]),
            str(peak["score"]),
            ".",
            ".",
            "name="+peak["name"]
        )
        try:
            gff3_peaks = gff3_peaks+"\t".join(tuple_site)+"\n"
        except Exception as e:
            print(e)
            print(peak)
    return gff3_peaks
