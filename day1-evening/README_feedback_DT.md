This is really well done! No need to change anything. I like your strategy for checking unique reads. In the future, instead of appending the information to a list (your `unique_reads` list), you might consider adding them to a set. Generally, it's faster to check if elements exist in a set rather than checking if they exist in a list.

Also, your strategy for ignoring header lines works, but it might be better to skip lines starting with `@` rather than only looking at lines starting with `SRR072893`. If you have a sam file with multiple queries, the first column may have different values.

Your advanced answers look great!! 