import cooler
from cooltools.eigdecomp import cis_eig
import numpy as np

cool = cooler.Cooler("K562_hg19_chr3_50K.cool")
mat = cool.matrix(balance=True)[:]

signal_track_file = open("hg19_GC_chr3_50K.txt")
signal_track = []

for line in signal_track_file:
    sign = float(line)
    signal_track.append(sign)

signal_track = np.array(signal_track)

eigen_vec = cis_eig(mat, 1, signal_track)[1][0]

bin_width = 50000
low = 1
high = bin_width

for val in eigen_vec:
    if val<=0:
        compartment = "B"
    else:
        compartment = "A"
    
    line = "\t".join(["chr3", str(low), str(high), compartment])    
    print(line)
    
    low += bin_width
    high += bin_width