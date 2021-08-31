import sys

def FASTAReader(file):
    # Get the first line, which should contain the sequence name
    line = file.readline()

    # Let's make sure the file looks like a FASTA file
    assert line.startswith('>'), "Not a FASTA file"
    
    # Get the sequence name
    seq_id = line[1:].rstrip('\r\n')

    # create a list to contain the 
    sequence = []

    # Get the next line
    line = file.readline()

    # Add a list to hold all of the sequences in
    sequences = []

    # Keep reading lines until we run out
    while line:
        # Check if we've reached a new sequence (in a multi-sequence file)
        if line.startswith('>'):
            # Add previous sequence to list
            sequences.append((seq_id, ''.join(sequence)))
            
            # Record new sequence name and reset sequence
            seq_id = line[1:].rstrip('\r\n')
            sequence = []
        else:
            # Add next chunk of sequence
            sequence.append(line.strip())
        
        # Get the next line
        line = file.readline()
    # Add the last sequence to sequences
    sequences.append((seq_id, ''.join(sequence)))

    return sequences
    
#open query and target files
target_file = open("/Users/cmdb/qbb2021/data/"+str(sys.argv[1]))
query_file = open("/Users/cmdb/qbb2021/data/"+str(sys.argv[2]))
  
#set k
k = int(sys.argv[3])

#convert to dictionary with seq_name and seqence as key and val
target_seq = FASTAReader(target_file)
query_seq = FASTAReader(query_file)
    
#function to get kmers and positions a single sequence
def kmer_finder(seq,k):
    kmer_dict = {}
    for i in range(len(seq)-k+1):
        kmer = seq[i:i+k]
        kmer_dict.setdefault(kmer,[])
        kmer_dict[kmer].append(i+1)
    return kmer_dict

#get kmers and positions of query seq
for seq in query_seq:
    query_kmers = kmer_finder(seq[1],k)

#loop through seq_names and seqs in target, get kmers and positions for each seq
for seq in target_seq:
    target_kmers = kmer_finder(seq[1], k)
    
    #for each kmer dictionary of a target seq, check if any kmers from query match, if so, print output as match
    for kmer in query_kmers.keys():
        if kmer in target_kmers:
            print(seq[0], query_kmers[kmer], target_kmers[kmer], kmer)
 
target_file.close()
query_file.close()
