Part 1: ChIP-seq

wget https://bx.bio.jhu.edu/data/msauria/cmdb-lab/g1e.tar.xz
tar xzf g1e.tar.xz

-x specify index filename prefix
-q input is a fastq file
-S output a sam file
-U unpaired read

export BOWTIE2_INDEXES=/Users/cmdb/data/indexes/bowtie2/mm10

bowtie2 -x mm10 -q -U CTCF_ER4.fastq -S CTCF_ER4.sam
bowtie2 -x mm10 -q -U CTCF_G1E.fastq -S CTCF_G1E.sam
bowtie2 -x mm10 -q -U input_ER4.fastq -S input_ER4.sam
bowtie2 -x mm10 -q -U input_G1E.fastq -S input_G1E.sam

-t input data file
-c control data file
-n specify output file name
--gsize specify genome size
--bdg store values in bedGraph file

conda activate chipseq
pip install --upgrade numpy

macs2 callpeak -t CTCF_ER4.sam -c input_ER4.sam -n ER4 --gsize=mm --bdg
macs2 callpeak -t CTCF_G1E.sam -c input_G1E.sam -n G1E --gsize=mm --bdg

bedtools intersect -v -a ER4_peaks.narrowPeak -b G1E_peaks.narrowPeak > peaks_gained.bed
 
bedtools intersect -v -a G1E_peaks.narrowPeak -b ER4_peaks.narrowPeak > peaks_lost.bed

wget https://raw.githubusercontent.com/bxlab/qbb2020/master/week5/Mus_musculus.GRCm38.94_features.bed

bedtools intersect -a Mus_musculus.GRCm38.94_features.bed -b G1E_peaks.narrowPeak > G1E_features.bed
bedtools intersect -a Mus_musculus.GRCm38.94_features.bed -b ER4_peaks.narrowPeak > ER4_features.bed

bedtools intersect -a Mus_musculus.GRCm38.94_features.bed -b peaks_gained.bed > peaks_gained_features.bed
bedtools intersect -a Mus_musculus.GRCm38.94_features.bed -b peaks_lost.bed > peaks_lost_features.bed

sort -k 4 G1E_features.bed | bedtools groupby -g 4 -c 4 -o count > G1E_bar.txt
sort -k 4 ER4_features.bed | bedtools groupby -g 4 -c 4 -o count > ER4_bar.txt
sort -k 4 peaks_gained_features.bed | bedtools groupby -g 4 -c 4 -o count > peaks_gained_bar.txt
sort -k 4 peaks_lost_features.bed | bedtools groupby -g 4 -c 4 -o count > peaks_lost_bar.txt