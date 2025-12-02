def pattern1(row):
    for i in range(row):
        for j in range(row,i,-1):
            print("*",end=" ")   
        print()
 
 
def pattern2(row):
    for i in range(row+1):
        for j in range(i,):
            print("*",end=" ")
        print()     
 

def pattern3(row):
    for i in range(row+1):
        for j in range(row-i):
            print(end=" ") 
        for j in range(i):
            print("*",end="")
        print()   
        

def pattern4(row):
    for i in range(row+1):
        for j in range(row-i):
            print(end=" ") 
        for j in range(2*i-1):
            print("*",end="")
        print() 
            
            
def pattern5(row):
     for i in range(row+1):
        for j in range(row-i):
            print(end=" ") 
        for j in range(2*i-1):
            print("*",end="")
        print()
        
     for i in range(row-1,0,-1):
         for j in range(row-i):
             print(end=" ")
         for j in range (2*i-1):
             print("*",end="")    
         print()  
   
                 
pattern1(6)  
pattern2(6)   
pattern3(6) 
pattern4(6) 
pattern5(6)  
        