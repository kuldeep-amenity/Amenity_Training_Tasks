## Copy Operation

### using shutil module used here for file opertion 
```python
import os
import shutil as sh

sh.copyfile("text.txt","text2.txt")
```
### copy content and folder

```python
sh.copytree('folder1','copyedfolder')
```
### Copy nested folder and files

```python
sh.copytree('nestedfolder','nestedfoldercopyed')
```

## Read and Write File

### Read File

```python
f=open("text.txt","r")
txt=f.read()
print(txt)

```

### Write File

```python
f = open('myfile.txt', 'a')
f.write('writing new file or create if do not exist')
f.close()
```
### Append File

```python
f = open('myfile.txt', 'a')
f.write('\nAppended new line to the file')
f.close()
```
### json File Read 

```python
import json

with open("file2.json","r",encoding='utf-8') as file:
    data=json.load(file)
print(data)    
```

### json File Write 

```python

data={
    "name":"Deep Tapodhan",
    "age":23
}

with open("file2.json","w",encoding="utf-8") as file:
    json.dump(data,file)
```

### append json File

```python
import json
with open("file2.json","r+",encoding="utf-8") as file:
    data=json.load(file)
    data["role"]="Trainee"
    file.seek(0)
    json.dump(data,file)
```
### read csv File

```python
import pandas as pd
pd.read_csv("students_data (1).csv")
```

```python
import csv
with open('students_data (1).csv',mode='r') as file:
    filecon=csv.reader(file)
    for i in filecon:
        print(i)
```

### write csv File

```python
fiels=["Name","age","role","Salary"]
data=[["Kuldeep",22,"Intern","0"],["Kuldeep",22,"Intern","0"],["Kuldeep",22,"Intern","0"],["Kuldeep",22,"Intern","0"]]
with open("newcsv.csv",mode="w") as file:
    csvwrite=csv.writer(file)
    csvwrite.writerow(fiels)
    csvwrite.writerows(data)
    
```

```python
with open("newcsv.csv",mode='r') as file:
    filecon=csv.reader(file)
    for i in filecon:
        print(i)
```

### append csv File

```python
with open("newcsv.csv",mode="a",newline='') as file:
    csvwrite=csv.writer(file)
    csvwrite.writerow(["Deep Tapodhan",23,"Trainee","15000"])
```
