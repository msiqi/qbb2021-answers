'''
python myscript_advanced.py BDGP6.Ensembl.81.gtf 3R 21378950 | column -t > myscript_advanced.out
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
    
    #check if line contains gene on mut_chrom 
    if (fields[0] == mut_chrom) and (fields[2] == "gene"): 
        #parse the final item in fields into subfields by ; delimiters
        subfields = fields[-1].split(';')
        for field in subfields:
            #if there is a gene name, obtain the gene name listed next to the label
            if "gene_name" in field:
                gene_name = field.split()[1]
            # if there is a gene biotype, obtain the gene biotype listed next to the label
            if "gene_biotype" in field:
                gene_biotype = field.split()[1]
        #append relevant info in a tuple to genes list
        genes.append((gene_name, start, end, gene_biotype))

#sorts genes by start position        
genes.sort(key = lambda x: x[1])

print("gene", "gene_dist", "iterations", "gene_biotype")

#make list to track nearest 20 genes
near20 = []

#run binary search 20 times to get 20 nearest genes
for i in range(20):
    #make copy of genes to serve as actively searched genes
    act_genes = list(genes)

    #make bool variable to determine end of search loop
    searching = True
    loop_count = 0

    #start binary search loop
    while searching:
        
        loop_count += 1

        #define hi lo and mid values based on active gene list
        lo = 0
        hi = len(act_genes)-1
        mid = int((hi+lo)/2)

        #to avoid infinite loop, handle cases where remaining list has just 2 items
        if len(act_genes) == 2:
            if act_genes[0][2]-mut_pos < act_genes[1][1]-mut_pos:
                near_gene = act_genes[0]
                gene_dist = act_genes[0][2]-mut_pos
            elif act_genes[1][1]-mut_pos < act_genes[0][2]-mut_pos:
                near_gene = act_genes[1]
                gene_dist = act_genes[1][1]-mut_pos
            else:
                near_gene = act_genes
                gene_dist = act_genes[1][1]-mut_pos
            searching = False
    
        #compare mut_pos with start_pos of mid gene in list
        #if less, change active gene list to lower half of genes, reloop
        elif mut_pos < act_genes[mid][1]:
            act_genes = act_genes[:mid+1]
        #if more, check if mut_pos if before end_pos of mid gene
        elif mut_pos > act_genes[mid][1]:
            if mut_pos <= act_genes[mid][2]: #if so, save mid gene and end loop
                searching = False
                near_gene = act_genes[mid]
                gene_dist = 0
            else: #if not, change active gene list to upper half of genes, reloop
                act_genes = act_genes[mid:]
        #if same, save mid gene and end loop
        else:
            searching = False
            near_gene = act_genes[mid]
            gene_dist = 0

    #add info about near gene to near20, remove this from genes to exclude from future searches
    near20.append([near_gene[0], abs(gene_dist), loop_count, near_gene[3]])
    genes.remove(near_gene)
    
# sort near20 by gene_dist
near20.sort(key = lambda x: x[1])

for gene in near20:
    print(gene[0], gene[1], gene[2], gene[3])

