def process_peaks_to_jsonT(sites):
    json_peaks_table = {
        'comments': [],
        'columns': [],
        'data': []
    }
    columns = ['start', 'end', 'score', 'strand', 'sequence', 'genes']
    return json_peaks_table


def process_peaks_to_gff3(peaks):
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
