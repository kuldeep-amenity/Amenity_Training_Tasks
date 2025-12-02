  # time complexity is n
def fibonaci(number):
    list=[] # space complexity is n
    if number <= 0:
        list.append(0)
    elif number == 1:
        list.append(0)
        list.append(1)
    else:
        list.append(0)
        list.append(1)
        a, b = 0, 1
        for _ in range(2,number):
            a, b = b, a + b
            list.append(b)
    return list   
        
        
number=int(input("Enter the number:"))
print(fibonaci(number))    