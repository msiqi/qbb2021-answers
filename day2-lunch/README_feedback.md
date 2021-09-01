Overall, the code looks great. You're making good use of comments and descriptive variable names. Also, the empty lines breaking up your code blocks makes it easy to follow the steps of your code. I especially appreciate the usage comment.

In the beginning of your code you read in the complete files. This is fine and definitely gives you the correct solution. But in the future you may be working with very large files and it isn't advantageous to load everything into memory upfront. It takes up RAM but also if this is a step in an analysis pipeline and you don't start outputting data until after you've loaded the whole file, then this would be a bottleneck in your pipeline. Food for thought.

I like that you're writing the output to standard out. This is really usefuly for piping it to downstream analysis steps.

The only issue that I see is that the assignment calls for skipping lines that have a gene-id not present in the mapping file if you don't have a third argument passed on the command line. It's a very simple fix. Otherwise everything looks great.

% completion: 98%