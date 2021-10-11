Getting the data

wget https://bx.bio.jhu.edu/data/msauria/cmdb-lab/mm10_refseq_genes_chr6_50M_60M.bed
wget https://bx.bio.jhu.edu/data/msauria/cmdb-lab/methylation_fastq.tar.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/mm10/chromosomes/chr6.fa.gz

mkdir index
mv chr6.fa.gz index
gzip -d index/chr6.fa.gz

tar xzf methylation_fastq.tar.gz

E4.0 - SRR3083926
E5.5 - SRR3083929

mkdir E4_fastqc
fastqc SRR3083926_1.chr6.fastq -o E4_fastqc/
The reads have little to no C, likely due to unmethylated C's being converted by bisulfite treatment

Bisulfite mapping with Bismark

bismark_genome_preparation index --parallel 7

bismark index -1 SRR3083926_1.chr6.fastq -2 SRR3083926_2.chr6.fastq -B E4.0
bismark index -1 SRR3083929_1.chr6.fastq -2 SRR3083929_2.chr6.fastq -B E5.5

deduplicate_bismark E4.0_pe.bam -o E4.0
deduplicate_bismark E5.5_pe.bam -o E5.5

samtools sort E4.0.deduplicated.bam -o E4.0_sorted.bam -O BAM
samtools index E4.0_sorted.bam

samtools sort E5.5.deduplicated.bam -o E5.5_sorted.bam -O BAM
samtools index E5.5_sorted.bam

bismark_methylation_extractor -p --bedgraph --comprehensive E4.0.deduplicated.bam
bismark_methylation_extractor -p --bedgraph --comprehensive E5.5.deduplicated.bam

gzip -d E4.0.deduplicated.bedGraph.gz E5.5.deduplicated.bedGraph.gz

Analysis 

awk 'BEGIN{OFS="\t"}{if ($4 == "+") print $3,$5 - 2000,$5,$13,$12,$4; else print $3,$6,$6 + 2000,$13,$12,$4;}' mm10_refseq_genes_chr6_50M_60M.bed | grep -v Rik | uniq -f 3 | sort -k2,2n > promoters.bed

bedtools intersect -a promoters.bed -b E4.0.deduplicated.bedGraph -wa -wb > E4.0_promoters.bed

bedtools intersect -a promoters.bed -b E5.5.deduplicated.bedGraph -wa -wb > E5.5_promoters.bed

bedtools groupby -i E4.0_promoters.bed -g 4 -c 10 -o sum > E4.0_scores.txt
bedtools groupby -i E5.5_promoters.bed -g 4 -c 10 -o sum > E5.5_scores.txt

See jupyter notebook for plots