Step 1
bwa index sacCer3.fa

Step 2
bwa mem -R "@RG\tID:A01_09\tSM:A01_09" -o A01_09.bam sacCer3.fa A01_09.fastq 
bwa mem -R "@RG\tID:A01_11\tSM:A01_11" -o A01_11.bam sacCer3.fa A01_11.fastq  
bwa mem -R "@RG\tID:A01_23\tSM:A01_23" -o A01_23.bam sacCer3.fa A01_23.fastq 
bwa mem -R "@RG\tID:A01_24\tSM:A01_24" -o A01_24.bam sacCer3.fa A01_24.fastq 
bwa mem -R "@RG\tID:A01_27\tSM:A01_27" -o A01_27.bam sacCer3.fa A01_27.fastq 
bwa mem -R "@RG\tID:A01_31\tSM:A01_31" -o A01_31.bam sacCer3.fa A01_31.fastq 
bwa mem -R "@RG\tID:A01_35\tSM:A01_35" -o A01_35.bam sacCer3.fa A01_35.fastq 
bwa mem -R "@RG\tID:A01_39\tSM:A01_39" -o A01_39.bam sacCer3.fa A01_39.fastq 
bwa mem -R "@RG\tID:A01_62\tSM:A01_62" -o A01_62.bam sacCer3.fa A01_62.fastq 
bwa mem -R "@RG\tID:A01_63\tSM:A01_63" -o A01_63.bam sacCer3.fa A01_63.fastq 

Step 3
samtools sort -O bam -o A01_09_sorted.bam A01_09.bam
samtools sort -O bam -o A01_11_sorted.bam A01_11.bam
samtools sort -O bam -o A01_23_sorted.bam A01_23.bam
samtools sort -O bam -o A01_24_sorted.bam A01_24.bam
samtools sort -O bam -o A01_27_sorted.bam A01_27.bam
samtools sort -O bam -o A01_31_sorted.bam A01_31.bam
samtools sort -O bam -o A01_35_sorted.bam A01_35.bam
samtools sort -O bam -o A01_39_sorted.bam A01_39.bam
samtools sort -O bam -o A01_62_sorted.bam A01_62.bam
samtools sort -O bam -o A01_63_sorted.bam A01_63.bam

Step 4-6
freebayes -f sacCer3.fa -p 2 --genotype-qualities *sorted.bam | vcffilter -f "QUAL > 20" | vcfallelicprimitives -k -g > out.vcf

Step 7
snpeff ann R64-1-1.99 out.vcf > out_ann.vcf

