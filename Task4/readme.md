# Values extract from the String using regular expresion

## Regx.py file contains function to extract email and contact number from the string using regular expresion

### code
``` python
def emailvalidation(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(email_regex, email):
        print("Email is Valid")
    else:
        print("Email is Invalid")
def mobilevalidator(contact):
    contact_regex = r"^\+?[0-9]{10,15}$"
    if re.fullmatch(contact_regex, contact):
        print("Number is Valid")
    else:
        print("Invalid Number")
    
emailvalidation("DeepTapodhan@gmail.com")
emailvalidation("DeepTapodhan@gmaiom")
mobilevalidator("9016568931")        
mobilevalidator("+919016568931") 
mobilevalidator("Aefbe543")        
```
### Output of the file is as below:
```text
Email is Valid
Email is Invalid
Number is Valid
Number is Valid
Invalid Number
```


## Text_Extraction.py file contains function to extract multiple values from the string using regular expresion

### Code for Regular Expression Patterns Used
``` python
email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Za-z]{2,3}'
Tel_pattern = r'tel[:\s]*([0-9]{6,15})'
abn_pattern = r'abn[:\s]*([0-9]{11})'

date_pattern = r'([0-9]{1,2}\s*[A-Za-z]+\s*[0-9]{4})'
due_date_pattern = r'duedate[:\s]*' + date_pattern
invoice_date_pattern = r'invoicedate[:\s]*' + date_pattern

amount_pattern = r'([0-9.,]+)'
amount_due_pattern = r'amountdue[:\s]*' + amount_pattern
amount_paid_pattern = r'amountpaid[:\s]*' + amount_pattern  
```

### later the regular expression were used with helpf of findall function to extract multiple values from the string.


### Input String
```text
string=
    "paymentadviceto:allhourselectricalwaabn:54788190299tel:92752839"
    "email:service@allhourselectricalwa.com.aucustomertuvakhusid"
    "invoicenumberinv-3649amountdue0.00duedate4jan2025"
    "amountenclosedentertheamountyouarepayingabovetaxinvoice"
    "tuvakhusidinvoicedate4jan2025invoicenumberinv-3649referencej2911"
    "abn54788190299allhourselectricalwaabn:54788190299tel:92752839"
    "email:service@allhourselectricalwa.com.au"
    "descriptionquantityunitpricegstamountaudinstalled1xclientsuppliedlight"
    "1.00150.0010%150.00job:j2911jobaddress:8salamanderstreet,dianella"
    "subtotal150.00totalgst10%15.00totalaud165.00"
    "addcreditcardprocessingfee2.81lessamountpaid167.81"
    "amountdueaud0.00duedate:4jan2025"
    "pleaseusetheinvoicenumberasthepaymentreference."
```

### output:
```text
Email: ['service@allhourselectricalwa.com', 'service@allhourselectricalwa.com']
Tel: ['92752839', '92752839']
ABN: ['54788190299', '54788190299', '54788190299']
Due Date: ['4jan2025', '4jan2025']
Invoice Date: ['4jan2025']
Amount Due: ['0.00']
Amount Paid: ['167.81']
```




