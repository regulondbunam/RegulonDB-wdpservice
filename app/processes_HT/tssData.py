

def process_tss_to_jsont(tss):
    json_tss_table = {
        'comments': [],
        'columns': [],
        'data': []
    }
    columns = ['start', 'end', 'score', 'strand', 'sequence', 'genes']
    return json_tss_table


def process_tss_to_gff3(tss):
    # NC_000913.3	RegulonDB	transcription_start_cluster	38	38	.	+	0	name=TSS_1
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