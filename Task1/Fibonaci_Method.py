def fibonaci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
def fiboseries(n):
    list=[] # space complexity is n
    # time complexity for bellow loop is n
    for i in range(n):
        list.append(fibonaci(i)) # n * n
    return list     

number=int(input("Enter the number:"))
print(fiboseries(number))    