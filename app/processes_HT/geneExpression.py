import os, sys
from app.utiles import errorRegister
import json 


def process_ge_to_jsonGQL(ge):
    jsongql = {'data': ge }
    jsongql = json.dumps( jsongql ) 
    return jsongql

def process_ge_to_csv(ge):
    table = {
        "columns": ["gene","leftEndPosition","rightEndPosition","TPM","FPKM",],
        "data": []
    }
    try:
      for ex in ge:
        data = []
        if ex["gene"]:
            gene = ex["gene"]["name"]
            lp = ex["gene"]["leftEndPosition"]
            rp = ex["gene"]["rightEndPosition"]
            data = [gene,lp,rp,ex["tpm"],ex["fpkm"]]
        table["data"].append(data)
    except:
      print('An exception occurred on process_ge_to_csv')
    return table;
    

def process_ge_to_jsont(ge):
    columns = """[
        {"Header": "Gene", "accessor": "_gene"},
        {"Header": "leftEndPosition", "accessor": "_lp"},
        {"Header": "rightEndPosition", "accessor": "_rp"},
        {"Header": "TPM", "accessor": "_tpm"},
        {"Header": "FPKM", "accessor": "_fpkm"},
        {"Header": "IGV position", "accessor": "_position"}
    ]"""
    data = []
    try:
        for ex in ge:
            if ex["gene"]:
                gene = f'[{{"_id":"{ex["gene"]["_id"]}","name":"{ex["gene"]["name"]}","bnumber": "{ex["gene"]["bnumber"]}"}}]'
                lp = ex["gene"]["leftEndPosition"]
                rp = ex["gene"]["rightEndPosition"]
                # NC_000913.3:603,209-621,582
                position = "NC_000913.3:"+str(lp)+"-"+str(rp)
                data.append(
                    f"""{{
                    "_id": "{ex["_id"]}",
                    "_tpm": "{ex["tpm"]}",
                    "_fpkm": "{ex["fpkm"]}",
                    "_lp": "{str(lp)}",
                    "_rp": "{str(rp)}",
                    "_gene": {gene},
                    "_position": "{position}"
                    }}"""
                )
        data = ",\n".join(data)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error = f"""on {str(fname)} def format_txt_gene, build txt [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
        errorRegister(error)
        print("error", e)
    return f'{{ "columns": {columns}, "data":[{data}] }}'


def process_ge_to_bedgraph(ge):
    # NC_000913.3 pl pr tpm  localhost:5000/ht/wdps/SRR10907670/ge/bedgraph
    # NC_000913.3	190	255	3780.619382
    print(ge[0])
    header = 'track type=bedGraph name="BedGraph Format" description="BedGraph format" visibility=full color=200,100,0 altColor=0,100,200 priority=20'
    bedgraph_ge = ""
    for ex in ge:
        try:
            posL = ""
            posR = ""
            if ex['gene']:
                posL = str(ex['gene']['leftEndPosition'])
                posR = str(ex['gene']['rightEndPosition'])
            tuple_ts = (
                "NC_000913.3",
                posL,
                posR,
                str(ex['tpm'])
            )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error = f"""on {str(fname)} def format_txt_gene, build txt [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
            errorRegister(error)
            print(e)
            print(ex)

        try:
            bedgraph_ge = bedgraph_ge+"\t".join(tuple_ts)+"\n"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error = f"""on {str(fname)} def format_txt_gene, build txt [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
            errorRegister(error)
            print(e)
            print(ex)
    return header+"\n"+bedgraph_ge
