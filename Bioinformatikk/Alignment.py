"""
Import libraries
"""
import numpy as np


"""
Open and read files in FASTA format
"""
gallus = open("Gallus_gallus.txt", "r")
human = open("Homo_sapiens.txt", "r")
blossom62 = open("blossum.txt", "r")
ogg1h = open("OGG1_human.txt", "r")
ogg1y = open("OGG1_yeast.txt", "r")
ecoli = open("ecoli.txt", "r")


def readInputfile(filename):
    """
    Function for reading the files
    The functions skips the first line, then reads the sequence
    
    filename: name of the text file to be read (SATA format)
    """
    sequence = []
    filename.readlines(1)
    for line in filename:
        for letter in line:
            if letter.isupper():
                sequence.append(str(letter))
    
    filename.close()
    return sequence
        

def makeBlossomDict(filename):
    """
    This function makes a dictionary of the blossom matrix.
    It is then easy to retrieve any letter combination from the blossum matrix
    
    filename: name of the text file to be read (blossum matrix)
    """
    letters = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V", "B", "Z", "X", "*"]
    numbers = []
    N = 24
    
    myDict = {}
    for line in filename:
        linenumbers = []
        for number in line.split(" "):
            try:
                if type(number) != int:
                    linenumbers.append(int(number))
                        
            except:
                pass
        numbers.append(linenumbers)
        linenumbers = []


    for i in range(N):
        for j in range(N):
            myDict[letters[i]+letters[j]] = numbers[i][j]
    filename.close()
    return myDict


def SmithWaterman(a, b, blossom, gap=1, penalty = 11, title = None):
    """
    This funtion does an alignment and calculates the score between to sequences
    with the Smith Waterman algorithm.
    It returns nothing, but will print the alignment and score.
    There is also an option to save the alignments to a texfile with a given name
    
    a: query in SATA format
    b: subject in  SATA format
    blossom: the blossom62 as a dictionary
    gap: gap penalty is set to 1 default, but can be chanced
    penalty: extension penalty is set to 11  default, but can be changed
    title: is set to None default, but can be set when calling the function
    """
    lena = len(a)
    lenb = len(b) 
 
    direct = [[[] for j in range(lenb+1)] for i in range(lena+1)]
    matrix = np.zeros((lena+1,lenb+1))
    V = matrix.copy()
    E = matrix.copy()
    E_dir = matrix.copy()
    F = matrix.copy()
    F_dir = matrix.copy()
    G = matrix.copy()
    G_dir = matrix.copy()
    
    for i in range(lena):
        E_dir[i+1][0] = -penalty
        F_dir[i+1][0] = -penalty
        
    for j in range(lenb):
        E_dir[0][j+1] = -penalty
        F_dir[0][j+1] = -penalty
        
    """
    Smith Waterman algorithm
    """
    for i in range(1, lena+1): 
        for j in range(1, lenb+1):
            G[i,j] = matrix[i-1, j-1] + blossom[a[i-1]+b[j-1]]
            G_dir[i,j] = diag = matrix[i-1, j-1] + blossom[a[i-1]+b[j-1]]
            
            F[i,j] = max(F[i-1,j]-gap, matrix[i-1,j]-gap-penalty)
            F_dir[i,j] = up = max(F_dir[i-1,j]-gap, matrix[i-1,j]-gap-penalty)
            
            E[i,j] = max(E[i,j-1]-gap, matrix[i,j-1]-gap-penalty)
            E_dir[i,j] = left = max(E_dir[i,j-1]-gap, matrix[i,j-1]-gap-penalty)
            
            V[i][j] = score = max(E[i,j], F[i,j], G[i,j],0)
            matrix[i, j] = max(E_dir[i,j], F_dir[i,j], G_dir[i,j],0)

            if score == diag: 
                direct[i][j].append('D')
    
            if score == up: 
                direct[i][j].append('U')

            if score == left: 
                direct[i][j].append('L')

    align_a = '' 
    align_x = '' 
    align_b = '' 
    i,j = np.unravel_index(matrix.argmax(), matrix.shape)
    print("Alignment score: ", int(V[i][j]))

    n = 0
    N = lena+lenb
    
    """
    Traceback
    """
    while (i > 0) or (j > 0):
        direction = direct[i][j]
            
        #print(matrix[i][j])
        #print(direction)
        if 'D' in direction: 
            align_a = a[i-1] + align_a 
            align_b = b[j-1] + align_b 
            if (a[i-1] == b[j-1]): 
                align_x = '|' + align_x 
            else: 
                align_x = ' ' + align_x 
            i -= 1 
            j -= 1 
            
        elif 'L' in direction: 
            align_a = '-' + align_a 
            align_b = b[j-1] + align_b 
            align_x = ' ' + align_x 
            j -= 1
            

        elif 'U' in direction: 
            align_a = a[i-1] + align_a 
            align_b = '-' + align_b 
            align_x = ' ' + align_x 
            i -= 1    


            
        if n > N:
            i = 0
            j = 0
            
        n+=1
            
    
    """
    printing the alignments
    """
    n = 6
    L = int(len(align_a)/n)
    
    for i in range(n+1):
        print("Query:  ", align_a[i*L:(i+1)*L])
        print("        ", align_x[i*L:(i+1)*L])
        print("Subject:", align_b[i*L:(i+1)*L])
        print("")
        
    """
    If title is given, the alignment is saved
    """
    if title:
        with open(title +".txt", "w") as outfile:
            outfile.write(align_a)
            outfile.write("\n")
            outfile.write(align_x)
            outfile.write("\n")
            outfile.write(align_b)
            
        outfile.close()
        

    return 0


"""
Retrieveing all the sequences in lists
"""
gallus_sequence = readInputfile(gallus)
human_sequence = readInputfile(human)
ogg1h_sequence = readInputfile(ogg1h)
oggy_sequence = readInputfile(ogg1y)
ecoli_sequence = readInputfile(ecoli)

"""
Retrieving the blossom dictionary
"""
blossomDict = makeBlossomDict((blossom62))

"""
test with short test sequences
"""
#a = "CACCCFFF"
#b = "CAWAWCCC"
#SmithWaterman(a, b, blossomDict, 1, 7)
#SmithWaterman(a, b, blossomDict, 1, 11)
#SmithWaterman(a, b, blossomDict, 1, 11, "test")

"""
test sequence from the exam
"""
SmithWaterman(ogg1h_sequence, oggy_sequence, blossomDict, 1, 11)
#SmithWaterman(ogg1h_sequence, oggy_sequence, blossomDict, 1, 11, "example alignment")

"""
main sequences
"""
SmithWaterman(gallus_sequence, human_sequence, blossomDict, 1, 11)
#SmithWaterman(gallus_sequence, human_sequence, blossomDict, 1, 11, "alignment") 

"""
last task with galus gallus and e-coli
"""
SmithWaterman(gallus_sequence, ecoli_sequence, blossomDict, 1, 11)
#SmithWaterman(gallus_sequence, ecoli_sequence, blossomDict, 1, 11, "ecoli alignment") 










