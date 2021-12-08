This looks good! For some reason in your second regression, you dropped the 10 stage, so your p-values are a bit off (-0.1). Otherwise your qqplots look great! Clustering and dendrogram both look good too! Solid work hardcoding FDR :D. You've noticed that the volcano plot is a bit off, but the reason is actually SUPER hard to see. When you're hard coding the FDR, you have the following: 
```
pvals_sex_ranked = pvals_sex
pvals_sex_ranked.sort()
```
Now it may look like you're creating a copy of the pvals_sex variable, but your actually just giving that data another variable name. So when you sort the pvalues, it's sorting both pvals_sex_ranked AND pvals_sex. That's why your pvals are getting messed up in the volcano plot. If you want to keep the code the way it is, take a look at the "copy" python module. No points off though.

6.9/7
