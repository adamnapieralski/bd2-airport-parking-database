from . import models
import datetime

def get_reservations(user):
    me = models.Klient.objects.get(user=user)
    attributes = [f.name for f in models.Rezerwacja._meta.concrete_fields]     
    data = models.Rezerwacja.objects.filter(klient = me).values_list(*attributes)    

    can_cancel = []
    current_date = datetime.datetime.now()

    for row in data:
        begin_date = row[2]
        
        if current_date < begin_date:
            can_cancel.append(row[0]) #add id 

    attributes = [attr.replace('_', ' ') for attr in attributes]
    
    return {'header': attributes, 'data': data, 'can_cancel': can_cancel}  

def cancel_reservation(id):
    try:
        models.Rezerwacja.objects.filter(id=id).delete()
    except:
        pass