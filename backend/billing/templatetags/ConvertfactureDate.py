from django import template

register = template.Library() 

@register.filter(name='oldFacture') 
def old_numbring(bill_number):
    old_billing = str(int(bill_number.strip("F")))
    
    return "ALG"+ old_billing  +" / 2021"