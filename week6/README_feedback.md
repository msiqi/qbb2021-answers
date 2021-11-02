Looks great! Two quick notes about how you generated your compartments.bed file. Your bins are all off by one but you actually shouldn't have to generate them manually, rather that information is stored in `cool.bins()[:]`. More importantly, the way you currently have a nan value in the eigenvector, it will default to writing that as an "A" in the bed file, rather than leaving it undefined.

4/4
