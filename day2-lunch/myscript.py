import sys

map_file = open("/Users/cmdb/qbb2021/data/"+sys.argv[1]).readlines()
data = open("/Users/cmdb/qbb2021/data/"+sys.argv[2]).readlines()
default = sys.argv[3]
mapping = dict()             

#look through data and add gene ids as keys to mapping
for line in data[1:]:
    fields = line.strip("\n").split("\t")
    gene_id = fields[8]
    mapping.setdefault(gene_id, default)

#look through map_file and assign protein ids to gene ids in mapping if gene id is a key
for line in map_file:
    fields = line.split("\t")
    gene_id = fields[0]
    protein_id = fields[1]
    if gene_id in mapping:
        mapping[gene_id] = protein_id

#print header with new column
print(data[0].strip("\n")+"\tprotein_id")

#print data lines with new protein_id value
for line in data[1:]:
    fields = line.strip("\n").split("\t")
    gene_id = fields[8]
    print(line.strip("\n")+"\t"+mapping[gene_id])
