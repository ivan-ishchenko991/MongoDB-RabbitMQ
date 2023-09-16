from mongoengine import *


connect(db='web14',
        host='mongodb+srv://IIshchenko1901:8COpNHsvUM7nlOlm@cluster0.mtkorsb.mongodb.net/?retryWrites=true&w=majority')

class Model(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    routing_key = StringField()
    boolean = BooleanField(default=False)
    meta = {'collection': 'models'}
