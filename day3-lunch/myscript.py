'''
python myscript.py BDGP6.Ensembl.81.gtf 3R 21378950 | column -t > myscript.out
'''

import sys

#store arguments from command line
gtf_file = sys.argv[1]
mut_chrom = sys.argv[2]
mut_pos = int(sys.argv[3])

#open .gtf file
f = open(gtf_file)

#generate list of tuples (gene name, start pos, end pos) for mut_chrome
#initialize list to store genes
genes = []

#loop through lines in .gtf file
for line in f:
    #ignore header lines
    if line.startswith("#"):
        continue
    #parse line by tab delimiters
    fields = line.strip("\r\n").split("\t")
    
    #store start and end positions
    start = int(fields[3])
    end = int(fields[4])
    
    #check if line contains gene on chromosome and relevant tags about the gene, only these are appended to list
    if (fields[0] == mut_chrom) and (fields[2] == "gene") and ('gene_biotype "protein_coding"' in line):
        #parse the final item in fields into subfields by ; delimiters
        subfields = fields[-1].split(';')
        for field in subfields:
            #if there is a gene name, obtain the gene name listed next to the label
            if "gene_name" in field:
                gene_name = field.split()[1]
        #append relevant info in a tuple to genes list
        genes.append((gene_name, start, end))

#sorts genes by start position        
genes.sort(key = lambda x: x[1])

#make bool variable to determine end of search loop
searching = True
loop_count = 0

#start binary search loop
while searching:
        
    loop_count += 1

    #define hi lo and mid values based on active gene list
    lo = 0
    hi = len(genes)-1
    mid = int((hi+lo)/2)

    #to avoid infinite loop, handle cases where remaining list has just 2 items
    if len(genes) == 2:
        if genes[0][2]-mut_pos < genes[1][1]-mut_pos:
            near_gene = genes[0]
            gene_dist = genes[0][2]-mut_pos
        elif genes[1][1]-mut_pos < genes[0][2]-mut_pos:
            near_gene = genes[1]
            gene_dist = genes[1][1]-mut_pos
        else:
            near_gene = genes
            gene_dist = genes[1][1]-mut_pos
        searching = False
    
    #compare mut_pos with start_pos of mid gene in list
    #if less, change active gene list to lower half of genes, reloop
    elif mut_pos < genes[mid][1]:
        genes = genes[:mid+1]
    #if more, check if mut_pos if before end_pos of mid gene
    elif mut_pos > genes[mid][1]:
        if mut_pos <= genes[mid][2]: #if so, save mid gene and end loop
            searching = False
            near_gene = genes[mid]
            gene_dist = 0
        else: #if not, change active gene list to upper half of genes, reloop
            genes = genes[mid:]
    #if same, save mid gene and end loop
    else:
        searching = False
        near_gene = genes[mid]
        gene_dist = 0
print("gene", "gene_dist", "iterations")
print(near_gene[0], abs(gene_dist), loop_count)
