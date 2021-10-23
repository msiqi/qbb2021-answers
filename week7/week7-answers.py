import sys
import numpy as np

#copy over the FASTAReader function
def FASTAReader(file):
    line = file.readline()
    seq_id = line[1:].rstrip('\r\n')
    sequence = []

    line = file.readline()
    sequences = []

    while line:
        if line.startswith('>'):
            sequences.append((seq_id, ''.join(sequence)))
            seq_id = line[1:].rstrip('\r\n')
            sequence = []
        else:
            sequence.append(line.strip())
        
        line = file.readline()
    
    sequences.append((seq_id, ''.join(sequence)))
    return sequences

#Take in arguments for filenames, filepaths, and scores
FASTA_file = open(sys.argv[1])
score_mat_file = open(sys.argv[2])
gap_penalty = float(sys.argv[3])
out_filepath = sys.argv[4]

#Read the FASTA file
FASTA_sequences = FASTAReader(FASTA_file)

#Assign sequences in FASTA file to sequence1 and sequence 2 
#Based it on species
for sequence in FASTA_sequences:
    seq_id = sequence[0]
    
    if "HUM" in seq_id:
        sequence1 = sequence[1]
    elif "MUS" in seq_id:
        sequence2 = sequence[1]

#Initialize lists to read score matrix
score_mat_list = []
score_mat_index = []

for line in score_mat_file:
    #The first line of the matrix is the AA or nucleotides being matched
    #Save these as indices for the score matrix
    if line.startswith(" "):
        score_mat_index = line.strip().split()
        continue
    #Take the scores on each line as a list
    #Convert to floats
    #Append to a list
    scores = line.strip().split()[1:]
    for i in range(len(scores)):
        scores[i] = float(scores[i])
    
    score_mat_list.append(scores)

#Convert score matrix to an numpy array
score_mat = np.array(score_mat_list)

#Initialize an F matrix and traceback matrix
#Traceback matrix: d = 0, h = 1, v = -1
F_matrix = np.zeros((len(sequence1)+1, len(sequence2)+1))
traceback = np.zeros((len(sequence1)+1, len(sequence2)+1))

#Add first row and column values to F matrix
for i in range(len(sequence1)+1):
    F_matrix[i,0] = i * gap_penalty
    traceback[i,0] = -1
    
for j in range(len(sequence2)+1):
    F_matrix[0,j] = j * gap_penalty
    traceback[0,j] = 1
    
#Fill in F matrix
for i in range(len(sequence1)+1):
    for j in range(len(sequence2)+1):
        #Get match score from score matrix
        index1 = score_mat_index.index(sequence1[i-1])
        index2 = score_mat_index.index(sequence2[j-1])
        match_score = score_mat[index1, index2]
        
        d = F_matrix[i-1, j-1] + match_score
        h = F_matrix[i, j-1] + gap_penalty
        v = F_matrix[i-1, j] + gap_penalty
        
        F_matrix[i,j] = max(d, h, v)
        
        if d == max(d, h, v):
            traceback[i,j] = 0
        elif h == max(d, h, v):
            traceback[i,j] = 1
        else:
            traceback[i,j] = -1

#follow the traceback matrix from the bottom right corner, form aligned sequences
i = len(sequence1)
j = len(sequence2)

sequence1_align = sequence1[i-1] 
sequence2_align = sequence2[j-1]

gaps1 = 0
gaps2 = 0
final_score = F_matrix[i, j]

while i>0 and j>0:
    
    if traceback[i, j] == 0:
        i -= 1
        j -= 1
        sequence1_align = sequence1[i-1] + sequence1_align
        sequence2_align = sequence2[j-1] + sequence2_align
        
    elif traceback[i, j] == 1:
        j -= 1
        sequence1_align = "-" + sequence1_align
        sequence2_align = sequence2[j-1] + sequence2_align
        gaps1 += 1
        
    else:
        i -= 1
        sequence1_align = sequence1[i-1] + sequence1_align
        sequence2_align = "-" + sequence2_align
        gaps2 += 1
        
    final_score += F_matrix[i, j]

#format the output nicely, write to output filepath
out_file = open(sys.argv[4], "w")

low = 0
high = 50
bin_size = 50

for bins in range(len(sequence1_align)//bin_size + 1):
    if i ==  len(sequence1_align)//bin_size:
        frag1 = sequence1_align[low:]
        frag2 = sequence2_align[low:]
    else:
        frag1 = sequence1_align[low:high]
        frag2 = sequence2_align[low:high]
        
    out_file.write(frag1+"\n")
    
    matcher = ""
    
    for i in range(len(frag1)):
        if frag1[i] == frag2[i]:
            matcher += "|"
        else:
            matcher += " "
    
    out_file.write(matcher+"\n")
    out_file.write(frag2+"\n"+"\n")
    
    low += 50
    high += 50
        
#print information in command line         
print("Number of gaps in sequence1: {}".format(gaps1))
print("Number of gaps in sequence2: {}".format(gaps2))
print("Score of final alignment: {}".format(final_score))

        
    
    