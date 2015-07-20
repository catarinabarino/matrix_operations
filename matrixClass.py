# Catarina Araujo
# 02/18/2015
# matrixClass.py - program that implements and tests a matrix class that performs several matrix operations

from math import sqrt
import string

def quadratic_roots(A,B,C):

    if A==0:
        raise ValueError("Your parabola needs a nonzero leading term")

    retVal = []
    D = B*B-4*A*C

    if D==0:
        retVal = [-float(B)/(2.0*float(A))]
      
    elif D>0:
        retVal = [(-float(B)+sqrt(D))/(2.0*float(A)), (-float(B)-sqrt(D))/(2.0*float(A))]

    return(retVal)


class Matrix:

    #global variables
    #tuple that includes all overloaded method calls
    methods = ('*', '+', '^', '~','%')   

    #initialization method
    def __init__(self, matrix):

        #initialize object-specific variables
        self.matrix = matrix
        if self.matrix:
            self.nCols = len(self.matrix[0])
            self.nRows = len(self.matrix)
        else:
            self.nRows = 0
            self.nCols = 0

        try:
            self.isMatrix = self.is_matrix()
            if not isinstance(self.matrix, list):
                raise TypeError("You did not enter a valid list!")
            
        except TypeError as x:
            raise

        else:
            try:
                if self.isMatrix == False:
                    raise ValueError("The list you entered is not a matrix!")

            except ValueError as x:
                raise


    def is_matrix(self):
    
        isMatrix = True

        #list comprehension to check if all rows contain the same number of columns. ie if matrix is a matrix
        sameNumElements = [len(eachRow) == self.nCols for eachRow in self.matrix]
        if not all(sameNumElements):
            isMatrix = False
    
        return(isMatrix)


    #displays instance matrix  
    def display(self):

        for r in range(self.nRows):
            for c in range(self.nCols):
                print self.matrix[r][c], ' ',
            print
   

   #adds instance matrix to matrix passed to method    
    def __add__(self, B):

        try:
            if self.nRows!=B.nRows or self.nCols!=B.nCols:
                raise IndexError("Cannot perform addition... matrix dimensions do not match.")

        except IndexError as x:
                raise
        
        else:                  
            resultMatrix = [[self.matrix[r][c] + B.matrix[r][c] for c in range(self.nCols)] for r in range(self.nRows)]

            C = Matrix(resultMatrix)

            #return Matrix object
            return(C)              

    #scale funcito overloaded asrmod (%)
    def scale(self, n):

        resultMatrix = [[n*elem for elem in eachRow] for eachRow in self.matrix]
        
        #create new Matrix object out of scaling result
        C = Matrix(resultMatrix)

        #return Matrix object
        return(C)


    def __mul__(self, B):
   
        try:
            if self.nRows != B.nCols:
                raise IndexError("Cannot perform multiplication... matrix dimensions do not match.")

        except IndexError as x:
            raise

        else:
            resultMatrix = []
            for r in range(self.nRows):
                resultMatrix.append([])
              
                for c in range(B.nCols):
                    product = 0 

                    for k in range(self.nCols):
                        product += self.matrix[r][k] * B.matrix[k][c]
                
                    resultMatrix[r].append(product)

            #create object out of 
            C = Matrix(resultMatrix)
            #return Matrix object
            return(C)


    def __pow__(self, n):

        #recursive function call if n>1
        if n>1:
            retVal = self*(self**(n-1))

        else:
            retVal = self
 

        return(retVal)


    def transpose(self):

        resultMatrix = [[r[i] for r in self.matrix] for i in range(self.nCols)]

        #create new Matrix object out of transpose results
        C = Matrix(resultMatrix)

        #return Matrix object
        return(C)
    
    def covar(self):

        n = float(self.nCols)
        return(self.mult(self.transpose()).scale(1.0/(n-1.0)))

    def eigenvals(self):

        if self.nRows!=2 or self.nCols!=2:
            raise ValueError("I only know how to compute eignevalues for 2x2 matrices")

        return(quadratic_roots(1, -self.matrix[0][0]+self.matrix[1][1]), self.matrix[0][0]+self.matrix[1][1]-self.matrix[0][1]+self.matrix[1][0]) 
        

#main test program
if __name__ == '__main__':

    #caps letters (A,B,C..) are all Matrix class objects
    
    print "Welcome to the Matrix Operations program!"
    answer = raw_input("Would you like to open a file? (y/n) ")
   
    if answer=='y':
       
        fileLoaded = False
        while not fileLoaded:

            fileName = raw_input("Enter name of file you would like to open: ")
            #open the file for reading
            try:
               robj = open(fileName, 'r')

            except IOError, e:
                print "I/O error: ", e

            else:

                try:
                    #create a list of Matrix objects from input file
                    matrixObjInList = [Matrix(eval(eachLine)) for eachLine in robj]

                except Exception, e:
                    print e

                else:
                    fileLoaded = True
           
    print "Your available matrices are:"
    #create alphabet iterator to iterate through letter of the alphabet
    alphabet = list(string.ascii_uppercase)
    matrices = {}
    #for loop iterating through alphabet and matrixObjList, zip() stops iteration when the shorter of the two lists ends 
    for eachMatrixObj, eachLetter in zip(matrixObjInList, alphabet):
         matrices.update({eachLetter: eachMatrixObj})
         print eachLetter + " = " + str(eachMatrixObj.matrix)

    #create a list to store results from operations as Matrix objects
    matrixObjOutList = []
    answer = 'x'
    #while loop controled by 'answer' 
    while answer != 'XX':
  
        answer = raw_input("Enter an operation you would like to perform. e.g. A*B. Use '+' for addition, '*' for multiplication, '^' for power, '~' for scaling, '%' for transpose, or 'XX' to quit: ")
        method_name = answer[1]
        if method_name in Matrix.methods:
 
            try:
                if method_name == '+':
                    X = matrices[answer[0]]+matrices[answer[2]]
                elif method_name == '*':
                    X = matrices[answer[0]]*matrices[answer[2]]
                elif method_name == '^':
                    X = matrices[answer[0]]**3
                elif method_name == '~':
                    X = matrices[answer[0]].scale(answer[2])
                elif method_name == '%':
                    X = matrices[answer[0]].transpose()
          
            except Exception, e:
                print 'Oops! Try again! Run time error: ', e

            else:
                print "Your result matrix is: "
                X.display()
                #append X.matrix to matrixObjOutList so that it is a list of lists
                matrixObjOutList.append(X.matrix)
         
    print "Your new matrices are: "
    print matrixObjOutList 
    answer1 = raw_input("Would you like to save your work? (y/n) ")
               
    if answer1=='y' or answer1=='Y':
              
        #open file for writing
        try:
            wobj = open(fileName+"out", 'w')

        except IOError, e:
            print "I/O error: ", e

        else:
            print "saving..."
            #read each list from matrixObjOutList and write it to the output file
            for eachList in matrixObjOutList: 
                wobj.write(str(eachList)+'\n')
                
            #close the connection to the output file
            wobj.close()

        #close the connection to the input file
        robj.close()

    print "Goodbye!"
