fs = open("/Users/cmdb/qbb2021-answers/day1-evening/SRR072893.sam")

num_alignments = 0 #create holder variable for number of alignments
num_perfect_alignments = 0 # create holder variable for number of perfect alignments
sum_MAPQ = 0 #create holder variable for sum of all MAPQ values
num_2L_range_alignments = 0 #create holder variable for number of alignments on 2L between 10000 and 20000
unique_reads = [] #create empty list to track unique reads
num_PCR_duplicates = 0 #create holder variable for number of PCR duplicate

for line in fs:
    if line.startswith("SRR072893"): #skip header lines, look only at lines with data
        num_alignments += 1 #count each line containing an alignment
        
        fields = line.strip("\n").split("\t") #parse line into values

        if fields[5] == "40M": #check CIGAR string for perfection of alignment
            num_perfect_alignments +=1 #counts each perfect alignment
        
        sum_MAPQ += int(fields[4]) #add MAPQ score to sum
        
        if fields[2] == "2L" and 10000<=int(fields[3])<=20000: #check to see if alignment is on 2L within range
            num_2L_range_alignments += 1 #count number of alignments fitting these criteria
        
        if not [fields[2], fields[3], fields[5]] in unique_reads: #add all unique reads to a running list
            unique_reads.append([fields[2], fields[3], fields[5]]) #check for uniqueness by chromosome number, bp, and CIGAR seq
        else:
            num_PCR_duplicates += 1 #if not unique, count as duplicate
            
print("Number of alignments: {}".format(num_alignments))
print("Number of perfect alignments: {}".format(num_perfect_alignments))
print("Average MAPQ score: {}".format(sum_MAPQ/num_alignments))
print("Number of alignments on 2L between 10000 and 20000 (inclusive): {}".format(num_2L_range_alignments))
print("Number of PCR duplicate: {}".format(num_PCR_duplicates))
