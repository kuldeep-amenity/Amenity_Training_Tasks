import re

def value_extract(text):
  
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Za-z]{2,3}'
    Tel_pattern = r'tel[:\s]*([0-9]{6,15})'
    abn_pattern = r'abn[:\s]*([0-9]{11})'

    date_pattern = r'([0-9]{1,2}\s*[A-Za-z]+\s*[0-9]{4})'
    due_date_pattern = r'duedate[:\s]*' + date_pattern
    invoice_date_pattern = r'invoicedate[:\s]*' + date_pattern

    amount_pattern = r'([0-9.,]+)'
    amount_due_pattern = r'amountdue[:\s]*' + amount_pattern
    amount_paid_pattern = r'amountpaid[:\s]*' + amount_pattern

    email = re.findall(email_pattern, text, re.I)
    Tel = re.findall(Tel_pattern, text, re.I)
    abn = re.findall(abn_pattern, text, re.I)
    due_date = re.findall(due_date_pattern, text, re.I)
    invoice_date = re.findall(invoice_date_pattern, text, re.I)
    amount_due = re.findall(amount_due_pattern, text, re.I)
    amount_paid = re.findall(amount_paid_pattern, text, re.I)
    
    print("Email:", email)
    print("Tel:", Tel)
    print("ABN:", abn)
    print("Due Date:", due_date)
    print("Invoice Date:", invoice_date)
    print("Amount Due:", amount_due)
    print("Amount Paid:", amount_paid)
    
    
    list=[email,Tel,abn,due_date,invoice_date,amount_due,amount_paid]
    
    return list



string = (
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
)

value_extract(string)
# print(value_extract(string))
