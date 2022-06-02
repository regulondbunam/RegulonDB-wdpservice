

def process_tus_to_jsont(tus):
    json_tus_table = {
        'comments': [],
        'columns': [],
        'data': []
    }
    columns = ['start', 'end', 'score', 'strand', 'sequence', 'genes']
    return json_tus_table


def process_tus_to_gff3(tus):
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
