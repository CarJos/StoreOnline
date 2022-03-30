from enum import Enum

class OrderStatus(Enum):
    '''Para limitar las opciones que el atributo status puede almacenar'''
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

choices = [(tag, tag.value) for tag in OrderStatus]