from mongoengine import DynamicDocument
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import EmailField
from mongoengine import IntField
from mongoengine import ListField
from mongoengine import ReferenceField
from mongoengine import FloatField
from mongoengine import DateTimeField


class TemperatureResult(DynamicDocument):
    result_temperature = FloatField(default=-40)
    real_temperature = FloatField(default=-40)
    date_time = DateTimeField(required=True)

