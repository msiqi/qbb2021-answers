This looks great! No need to change anything. Some notes/suggestions though:
1. When you're recording the commands you used, there's no need to copy the prompt (e.g. instead of writing `(base) (12:36:22)/qbb2021-answers/day1-lunch/$cp /Users/cmdb/qbb2021/data/K4me3.bed .` you can just write `cp /Users/cmdb/qbb2021/data/K4me3.bed .`).
2. Your command for question 4 works, but instead of using `uniq` twice, bedtools intersect also has a `-u` flag that only prints one intersection per feature in `A`, so you can skip your first `uniq`.
