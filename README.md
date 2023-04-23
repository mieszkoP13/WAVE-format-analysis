# WAVE-format-analysis

## Chunk parsing
There are two main approaches, algorithms that I came up with when it comes to WAVE file format chunk parsing

### Sequential method
This method is based on parsing candidates for a chunk one by one in certain order; basic steps of this solution:
1. Find candidate in a file from a list of potential chunks
2. Move file cursor to that place
3. Read that chunk; cursor has moved to the end of that chunk
4. Repeat above steps until EOF
5. Assert all candidates and remove them from actual list of chunks

Advantages of this method:
1. Its perfect when file is well organized, has no additional or unconventional chunks that we did not consider in the program and chunk ID's don't occur randomly or numerously in a file in different places

Disadvantages of this method:
1. It performs poorly when dealing with files which structures are imperfect, unconventional or damaged, even one unforeseen text occurrence in the middle of a file when parsing might well affect whole structure and chunks will not be read properly

### Non-Sequential method
This method is based on finding all candidates for a chunk and parsing them; basic steps of this solution:
1. Take one candidate from a list of potential chunks
2. Find all occurrences of a candidate by chunk ID
3. Read all found occurrences
4. Repeat for the rest of potential chunks from the list until EOF
5. Assert all candidates and remove them from actual list of chunks

Advantages of this method:
1. It deals greatly with files which structures are imperfect, unconventional or damaged, every chunk ID occurrence is taken into consideration regardless of chunks interference/invade

Disadvantages of this method:
1. Chunks received from parsing procedure can repeat so its possible to get file structure with multiple chunk of the same type which is not representative of WAVE file format