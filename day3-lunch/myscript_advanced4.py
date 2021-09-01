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

#make a copy of genes to track actively searched genes
act_genes = list(genes)

#start binary search loop
while searching:
        
    loop_count += 1

    #define hi lo and mid values based on active gene list
    lo = 0
    hi = len(act_genes)-1
    mid = int((hi+lo)/2)

    #to avoid infinite loop, handle cases where remaining list has just 2 items
    if len(act_genes) == 2:
        # if closer to end of first gene, take first gene
        if mut_pos-act_genes[0][2] < act_genes[1][1]-mut_pos:
            near_gene = act_genes[0]
            gene_dist = mut_pos-act_genes[0][2]
        #if closer to start of second gene, take second gene
        elif act_genes[1][1]-mut_pos < mut_pos-act_genes[0][2]:
            near_gene = act_genes[1]
            gene_dist = act_genes[1][1]-mut_pos
        #if equidistant, arbitarily take the first gene, might fix this later
        else:
            near_gene = act_genes[0]
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
        
print(near_gene[0], gene_dist, loop_count) 


#make list to hold next 19 nearest genes, store index of nearest gene
near19 = []
near_idx = genes.index(near_gene)

#make variables that keep track of what items downstream or upstream of near gene we are comparing
down = 1
up = 1

#start counter for additional nearest genes to be added
counter = 19

#check genes next to near_gene and obtain 20 nearest genes, in order of proximity to mut_pos
while counter>0:
    gene_up = genes[near_idx-up]
    gene_down = genes[near_idx+down]
    
    if mut_pos-gene_up[2] < gene_down[1]-mut_pos:
        near19.append((gene_up, mut_pos-gene_up[2]))
        up += 1
        counter -=1
    elif mut_pos-gene_up[2] > gene_down[1]-mut_pos:
        near19.append((gene_down, gene_down[1]-mut_pos))
        down +=1
        counter -=1
    else:
        near19.append((gene_up, mut_pos-gene_up[2]))
        near19.append((gene_down, gene_down[1]-mut_pos))
        up += 1
        down +=1
        counter -= 2

#sort genes by gene_dist and print gene_name and distance
near19.sort(key = lambda x: x[1])

for gene in near19:
    print(gene[0][0], gene[1])      


