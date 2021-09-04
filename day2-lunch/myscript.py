import sys

#use to call: python myscript.py fly_mapping.txt tdata.ctab default

#open input files
map_file = open("/Users/cmdb/qbb2021/data/"+sys.argv[1])
data = open("/Users/cmdb/qbb2021/data/"+sys.argv[2])

#set a default protein_id based on input, made an empty dictionary for gene_id to protein_id mapping
default = ""
if len(sys.argv) == 4:
	default = sys.argv[3]
mapping = dict()             

#look through map_file and add gene id and protein id pairs to dictionary
for line in map_file:
    fields = line.strip("\n").split("\t")
    gene_id = fields[0]
    protein_id = fields[1]
    mapping[gene_id] = protein_id

#print header
print(data.readline().strip("\n"))

#print data lines with new protein id value in place of gene id
for line in data:
    fields = line.strip("\n").split("\t")
    new_line = fields[0]
    if fields[8] in mapping:
        fields[8] = mapping[fields[8]]
    elif default:
        fields[8] = default
    else:
        continue
    
    for field in fields[1:]:
            new_line += "\t"+ field
    print(new_line)
