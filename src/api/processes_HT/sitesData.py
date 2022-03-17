def process_sites_to_jsonT(sites):
    json_sites_table = {
        'comments': [],
        'columns': [],
        'data': []
    }
    columns = ['start', 'end', 'score', 'strand', 'sequence', 'genes']
    return json_sites_table


def process_sites_to_gff3(sites):
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
