people = {'Alice':{'phone':'9102', 'addr':'Bar street 42'},
                'Beth':{'phone':'3158', 'addr':'Baz avenue'}
                }

labels = {'phone': 'people name', 'addr': 'address'}
name = raw_input('Name: ')
request = raw_input('Phone number(p) or address(a): ')
if request == 'p' : key = 'phone'
else : key = 'addr'
print people[name][key]
print labels[key]