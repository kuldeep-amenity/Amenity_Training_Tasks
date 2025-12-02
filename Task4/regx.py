import re

class RegularExpressionValidator:

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


RegularExpressionValidator.emailvalidation("DeepTapodhan@gmail.com")
RegularExpressionValidator.emailvalidation("DeepTapodhan@gmaiom")

RegularExpressionValidator.mobilevalidator("9016568931")        
RegularExpressionValidator.mobilevalidator("+919016568931") 
RegularExpressionValidator.mobilevalidator("Aefbe543")
