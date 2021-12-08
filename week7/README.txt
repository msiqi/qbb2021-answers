Getting your data

wget https://github.com/bxlab/qbb2021/raw/main/week7/needleman-wunsch.tar.gz
tar -xzf needleman-wunsch.tar.gz

Running script in command line

python week7-answers.py CTCF_38_M27_AA.faa BLOSUM62.txt -10 AA_sequence_alignment.txt

Number of gaps in sequence1: 9
Number of gaps in sequence2: 0
Score of final alignment: 3801.0

python week7-answers.py CTCF_38_M27_DNA.fna HOXD70.txt -300 DNA_sequence_alignment.txt

Number of gaps in sequence1: 46
Number of gaps in sequence2: 77
Score of final alignment: 266300.0