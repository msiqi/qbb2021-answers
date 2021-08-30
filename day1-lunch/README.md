1C
(base) (12:36:22)~/qbb2021-answers/day1-lunch/$cp /Users/cmdb/qbb2021/data/K27me3.bed .
(base) (12:36:32)~/qbb2021-answers/day1-lunch/$cp /Users/cmdb/qbb2021/data/K4me3.bed .
(base) (12:37:02)~/qbb2021-answers/day1-lunch/$cp /Users/cmdb/qbb2021/data/K9me3.bed .
(base) (12:37:10)~/qbb2021-answers/day1-lunch/$cp /Users/cmdb/qbb2021/data/LADs_Kc.bed .
(base) (12:37:20)~/qbb2021-answers/day1-lunch/$cp /Users/cmdb/qbb2021/data/S2_9state.bed .
(base) (12:37:30)~/qbb2021-answers/day1-lunch/$cp /Users/cmdb/qbb2021/data/dm6.chrom.sizes .
(base) (12:37:40)~/qbb2021-answers/day1-lunch/$cp /Users/cmdb/qbb2021/data/fbgenes.bed .

2A
(base) (12:45:01)~/qbb2021-answers/day1-lunch/$wc -l *.bed > feature_count.txt

2C
There are the most methylation regions for K27 compared to the other lysine residue on H3
There are about 30,000 fly-based genes

3A
(base) (12:58:33)~/qbb2021-answers/day1-lunch/$cut -f 1 fbgenes.bed | uniq -c > fbgenes.info

3C
Chromosome 2R has the most genes
There are 8 different fly-based chromosomes

4A
(base) (13:35:15)~/qbb2021-answers/day1-lunch/$bedtools intersect -a fbgenes.bed -b K9me3.bed | cut -f 1,4 | uniq | cut -f 1 | uniq -c > chr-with-fbgenes-k9.txt

4D
Chromosome X has the most genes with K9 methylation
There is K9 methylation on 7 different chromosomes
