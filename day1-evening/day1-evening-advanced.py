fs = open("/Users/cmdb/qbb2021-answers/day1-evening/SRR072893.sam") #open .sam file

num_reverse_reads = 0 #create holder variable for number of reads mapping to reverse strand
num_q30_reads = 0 #create holder variable for number of reads with quality score over 30
num_indels = 0 #create holder variable for total number of indels across all reads

for line in fs: #loop through each line in the .sam file
    if line.startswith("SRR072893"): #look only at alignments
       
        fields = line.strip("\n").split() #parse line into column values
        FLAG = int(fields[1]) #obtain the flag value as an integer
        if FLAG&(1<<4): #check for 0x10 flag indicating mapping to reverse strand, at index 4
            num_reverse_reads += 1
        
        sum_quality_vals = 0 #create holder variable for sum of quality values for a read
        quality_vals = fields[10] #obtain string with phred+33 quality values
        
        for char in fields[10]: #go through each quality value corresponding to a base in the aligned sequence
            qscore = ord(char)-33 #obtain q-score from ascii value of character in quality_vals minus 33
            sum_quality_vals += qscore #add q-score to sum
        if (sum_quality_vals/len(fields[10])) >= 30: #check if average q-score is equal to or greater than 30
            num_q30_reads += 1 # count number of reads fitting these criteria
        
        CIGAR = fields[5] #obtain the CIGAR string
        for char in CIGAR: #loop through each character in the CIGAR string
            if char == 'I' or char =='D': #check for presence of insertion or deletion
                num_indels += 1 #count number of indels across all reads
            
print("Number of reads mapping to reverse strand: {}".format(num_reverse_reads))
print("Number of reads with average quality value >= 30: {}".format(num_q30_reads))
print("Number of indels across all reads: {}".format(num_indels))
