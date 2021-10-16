Installing CoolTools

conda create -n hic cooltools cooler matplotlib numpy bedtools ucsc-bigWigToBedGraph
conda activate hic
conda install jupyter

Getting data

wget https://bx.bio.jhu.edu/data/msauria/cmdb-lab/3Dgenome_encode.tar.gz
tar xzf 3Dgenome_encode.tar.gz
bigWigToBedGraph K562_hg19_H3K27me3_chr3.bw K562_hg19_H3K27me3_chr3.bg

Compartment analysis

See jupyter notebook

python compartments.py > compartments.bed

Expression vs. Repression

Normalize H3K27me3 signals
awk 'BEGIN{OFS="\t"}{$5=($3-$2)*$4; print $1,$2,$3,$4,$5}' K562_hg19_H3K27me3_chr3.bg > K562_hg19_H3K27me3_chr3_norm.bg

Map sum of normalized H3K27me3 signals to chr3 genes
bedtools map -a K562_hg19_FPKM_chr3.bed -b K562_hg19_H3K27me3_chr3_norm.bg -c 5 -o sum > K562_hg19_FPKM_chr3_map.bed

Normalize H3K27me3 signals again
awk 'BEGIN{OFS="\t"}{$7=$7 / ($3-$2); print $1,$2,$3,$4,$5,$6,$7}' K562_hg19_FPKM_chr3_map.bed > K562_hg19_FPKM_chr3_mapnorm.bed

Map compartments to chr3 genes with >50% overlap
bedtools map -f 0.5 -a K562_hg19_FPKM_chr3_mapnorm.bed -b compartments.bed -c 4 -o distinct > K562_hg19_FPKM_compartment_chr3_mapnorm.bed