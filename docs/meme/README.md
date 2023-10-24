# Position specific scoring matrices for TFs v5.0

### Description of the dataset

The PSSMs version 5.0 are built using the annotated binding sites of TFs from RegulonDB version 12.0. A matrix is built for all TFs with four or more annotated sites. 

### Data Summary

Two subsets are generated: 

1. **Matrices for Confirmed & Strong TFBS**.

   - Total number of matrices including binding sites with `strong` or `confirmed` evidence: `97`

2. **Matrices for All TFBS**.

   - Total number of matrices including all binding sites: `109`


### Method

#### Programs

 * [MEME version 5.4.0](https://meme-suite.org/meme/doc/install.html?man_type=web)

#### Datasets, databases, files

1. *Genome Sequence*

  - Genome Sequence Identifier U00096.3.  
  - E. coli’s Genome Version: version 3 (U00096.3).  

2. *RegulonDB dataset*  
  2.1 [Transcription Factor Regulatory Interactions - TF-RISet.tsv file](https://regulondb.ccg.unam.mx/datasets/TFSet) version 12.0

3. *Protocol*

  1. TFBSs were retrieved from RegulonDB web page TF-RISet.tsv. Two types of matrices were generated: a) matrices including only binding sites with `Strong` or `Confirmed` evidence, and b) matrices including all annotated binding sites.
  2. Only unique genomic sites were retained, and TFs with four or more sites were analyzed. In the case of CRP, binding sites with unusual sizes were excluded (it means that small sites or those outside the average were excluded).
  3. The binding site sequences were retrieved, including 3 base pairs on each side of the binding site. 
  4. The MEME version 5.4.0 was executed to generate matrices of different sizes (median length of the binding site +/- 3 base pairs). MEME was run in "One Occurrence Per Sequence" mode, excluding the search in the reverse complement, specifying "dna" as the alphabet, and utilizing the U00096.3 Markov background model file for normalization.

### Results

Total number of matrices including binding sites with `strong` or `confirmed` evidence: `97`

```
Ada		CsgD	Fur		IHF		MqsA	PhoB	RutR
AgaR	CysB	GadE	IclR	MraZ	PhoP	SdiA
AraC	CytR	GadW	IscR	Nac		PlaR	SlyA
ArcA	Dan		GadX	LeuO	NagC	PurR	SoxR
ArgP	DcuR	GalR	LexA	NanR	PutA	SoxS
ArgR	DeoR	GalS	Lrp		NarL	PuuR	SrsR
AscG	DnaA	GcvA	MalT	NarP	QseB	TorR
BaeR	EvgA	GlaR	MarA	NhaR	RacR	TrpR
BasR	FNR		GlpR	MelR	NrdR	RbsR	TyrR
BtsR	FadR	GlrR	MetJ	NsrR	RcdA	UlaR
CRP		FeaR	GntR	MetR	NtrC	RcsB	XylR
CaiF	FhlA	H-NS	Mlc		OmpR	RelBE	YdeO
CpxR	Fis		HipAB	MlrA	OxyR	RhaS	ZraR
Cra		FlhDC	HipB	ModE	PdhR	Rob
```


Total number of matrices including all binding sites: `109`

```
Ada		CysB	GadW	LexA	NarL	RacR	TorR
AgaR	CytR	GadX	Lrp		NarP	RbsR	TrpR
AraC	Dan		GalR	MalT	NhaR	RcdA	TyrR
ArcA	DcuR	GalS	MarA	NrdR	RcsAB	UlaR
ArgP	DeoR	GcvA	MelR	NsrR	RcsB	UxuR
ArgR	DnaA	GlaR	MetJ	NtrC	RcsB-BglJ	XylR
AscG	EvgA	GlpR	MetR	OmpR	RelBE	YciT
AsnC	ExuR	GlrR	Mlc		OxyR	RhaS	YdeO
BaeR	FNR		GntR	MlrA	PdhR	Rob		YfeC
BasR	FadR	H-NS	MntR	PhoB	RstA	YidZ
BtsR	FeaR	HipAB	ModE	PhoP	RutR	YjjQ
CRP		FhlA	HipB	MqsA	PlaR	SdiA	ZraR
CaiF	Fis		IHF		MraZ	PurR	SlyA	Zur
CpxR	FlhDC	IclR	Nac		PutA	SoxR
Cra		Fur		IscR	NagC	PuuR	SoxS
CsgD	GadE	LeuO	NanR	QseB	SrsR
```

Each TF has a directory with the MEME results: 


- `index.html`: HTML file with the results, it integrates the logo and meme results. 
- Logo files
   - `logo1.png`	
   - `logo1.eps`	
   - `logo_rc1.png`
   - `logo_rc1.eps`	
- `meme.xml` : resuls in XML format
- `meme.txt`: results in text format	
- `ri_sites.fasta`: the input, non redundant TF binding sites in fasta format



### Credits

See [Our data Contributors](https://regulondb.ccg.unam.mx/manual/aboutUs/credits#heading-2).