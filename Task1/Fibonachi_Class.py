class fibo:
    # time complexity is n
    def fibonaci(self,number):
        list=[] # space complexity is n
        if number <= 0:
            list.append(0)
        elif number == 1:
            list.append(1)
        else:
            list.append(0)
            a, b = 0, 1
            for _ in range(2, number + 1):
                a, b = b, a + b
                list.append(b)
        return list   
        
    # def fiboseries(self,n):
    #     list=[] # space complexity is n
    #     # time complexity for bellow loop is n
    #     for i in range(n):
    #         list.append(self.fibonaci(i))
    #     return list
    
if __name__=="__main__":
    f=fibo()
    number=int(input("Enter the number:"))
    result=f.fibonaci(number)
    print(result)