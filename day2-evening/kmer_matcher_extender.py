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

#list to keep track of matches
kmer_matches = []

#loop through seq_names and seqs in target, get kmers and positions for each seq
for seq in target_seq:
    target_kmers = kmer_finder(seq[1], k)
    
    #for each kmer dictionary of a target seq, check if any kmers from query match
    for kmer in query_kmers.keys():
        if kmer in target_kmers:
            #look at all the pairs of t_pos and q_pos for a kmer
            for t_pos in target_kmers[kmer]:
                for q_pos in query_kmers[kmer]:
                    #extend kmer match to longest matching sequence
                    ext = 0
                    kmer_ext= kmer
                    perf_match = True
                    while perf_match:
                        if t_pos+k+ext<=len(seq[1])-1 and q_pos+k+ext<=len(query_seq[0][1]):
                            if seq[1][t_pos+k+ext]==query_seq[0][1][q_pos+k+ext]:
                                kmer_ext += seq[1][t_pos+k+ext]
                                ext += 1
                            else:
                                perf_match = False
                        else:
                            perf_match = False
                    #add details of match to list of matches
                    kmer_matches.append([ext, seq[0], t_pos, q_pos, kmer_ext])
#sort matches by length of match
kmer_matches = sorted(kmer_matches, key = lambda x: x[0], reverse = True)

for match in kmer_matches:
    print("\t".join([str(match[1]), str(match[2]), str(match[3]), str(match[4])]))
    
target_file.close()
query_file.close()
