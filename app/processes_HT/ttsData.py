

def process_tts_to_jsont(tts):
    json_tts_table = {
        'comments': [],
        'columns': [],
        'data': []
    }
    columns = ['start', 'end', 'score', 'strand', 'sequence', 'genes']
    return json_tts_table


def process_tts_to_gff3(tts):
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
