from tortoise.models import Model
from tortoise import fields

class User(Model):
    name = fields.CharField(max_length=255)
    usr_name = fields.CharField(max_length=255)
