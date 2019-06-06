from mongoengine import DynamicDocument
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import EmailField
from mongoengine import IntField
from mongoengine import ListField
from mongoengine import ReferenceField
from mongoengine import FloatField
from mongoengine import DateTimeField


class TemperaturePredict(DynamicDocument):
    pointID_305456 = FloatField(default=0)
    create_time = DateTimeField(required=True)
    out_temperature = FloatField(default=0)
    out_humidity = FloatField(default=0)
    in_temperature = FloatField(default=0)
    in_humidity = FloatField(default=0)
    power_consumption = FloatField(default=0)
    access_control = IntField()


