class fibo:
    # time complexity is n
    def fibonaci(self,number):
        if number <= 0:
            return 0
        elif number == 1:
            return 1
        else:
            a, b = 0, 1
            for _ in range(2, number + 1):
                a, b = b, a + b
            return b
        
    def fiboseries(self,n):
        list=[] # space complexity is n
        # time complexity for bellow loop is n
        for i in range(n):
            list.append(self.fibonaci(i))
        return list
    
if __name__=="__main__":
    f=fibo()
    number=int(input("Enter the number:"))
    result=f.fiboseries(number)
    print(result)