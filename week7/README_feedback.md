This almost perfect, just a few small things: When you're populating the matrices, you're currently overwriting the first row and column. Start from the second (index 1) row and second column. Also, when calculating the alignment score, it should just be the number in the bottom right of the F_matrix, you don't need to add every number along the path. The score at the bottom right should be the score we get if we add all the gaps, matches and mismatches in our final alignment as is. (-0.25)

4.75/5
