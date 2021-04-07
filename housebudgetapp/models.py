from tortoise import Tortoise, fields
from tortoise.models import Model


class Group(Model):
    class Meta:
        table = 'grupe'
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=60)

    users: fields.ReverseRelation["User"] = fields.ReverseRelation

class User(Model):
    class Meta:
        table = 'users'
        
    id = fields.UUIDField(pk = True)

    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50, null=True)
    monthly_income = fields.FloatField()

    group = fields.ForeignKeyField('models.Group', index=True, null=False, related_name='users')

    def __str__(self):
        return f"{self.id} {self.first_name}"

    #username mozda pitaj igora
    #pass mozda

#    group: fields.ForeignKeyRelation['Group'] = fields.ForeignKeyField(
#        'models.Group', related_name='users', index=True, null=True
#    )

    # container: fields.ForeignKeyRelation['Container'] = fields.ForeignKeyField(
    #     'waste.Container', related_name='alarms', index=True, null=False, on_delete=fields.CASCADE,
    #     source_field='id_container')


class Trosak(Model):

    class Meta:
        table = 'troskovi'

    id = fields.UUIDField(pk = True)
    name = fields.CharField(max_length=60)
    price = fields.FloatField()

    user = fields.ForeignKeyField('models.User', index=True)

#    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
#        'User', related_name='troskovi', index=True, null=False, on_delete=fields.CASCADE
#    )






