#open source file to be parsed
source_file = open("/Users/cmdb/qbb2021-answers/day2-lunch/fly.txt").readlines()

#make a dictionary to store gene and protein ids
fly_mapping = dict()

#loop through lines in source_file
for line in source_file:
    #look only at lines with fly genes
    if "DROME" in line: 
        
        #get gene_id and protein_id in their column ranges, strip all white space
        gene_id = line[51:].strip()
        protein_id = line[40:51].strip()
        
        #check that gene_id is not empty before adding to dictionary
        if gene_id != "":
            fly_mapping[gene_id] = protein_id
            
for gene_id, protein_id in fly_mapping.items():
    print("{0}\t{1}".format(gene_id, protein_id))
