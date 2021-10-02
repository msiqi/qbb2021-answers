Getting the data

SRR3083926 - E4.0
SRR3083929 - E5.5

fastqc SRR3083926_1.chr6.fastq -o output
The report of per base sequence shows almost no cytosines (C) in the reads.
This is likely because these are unmethylated cytosines that were converted by bisulfite treatment.

Bisulfate mapping with Bismark

bismark_genome_preparation --parallel 7 index
bismark index -1 SRR3083926_1.chr6.fastq,SRR3083929_1.chr6.fastq -2 SRR3083926_2.chr6.fastq,SRR3083929_2.chr6.fastq -o output
in output: deduplicate_bismark SRR3083926_1.chr6_bismark_bt2_pe.bam SRR3083929_1.chr6_bismark_bt2_pe.bam 

samtools sort SRR3083926_1.chr6_bismark_bt2_pe.deduplicated.bam -o SRR3083926_sorted.bam
samtools sort SRR3083929_1.chr6_bismark_bt2_pe.deduplicated.bam -o SRR3083929_sorted.bam

samtools index SRR3083926_sorted.bam
samtools index SRR3083929_sorted.bam

bismark_methylation_extractor --bedgraph --comprehensive SRR3083926_1.chr6_bismark_bt2_pe.deduplicated.bam SRR3083929_1.chr6_bismark_bt2_pe.deduplicated.bam 

