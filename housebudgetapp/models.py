from tortoise import Tortoise, fields
from tortoise.models import Model


class User(Model):
    class Meta:
        table = 'users'
    id = fields.UUIDField(pk = True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50, null=True)
    monthly_income = fields.FloatField()
    #username mozda pitaj igora
    #pass mozda

    group: fields.ForeignKeyRelation['Group'] = fields.ForeignKeyField(
        'app.Group', related_name='users', index=True, null=True
    )

    # container: fields.ForeignKeyRelation['Container'] = fields.ForeignKeyField(
    #     'waste.Container', related_name='alarms', index=True, null=False, on_delete=fields.CASCADE,
    #     source_field='id_container')




class Trosak(Model):
    class Meta:
        table = 'troskovi'
    id_trosak = fields.UUIDField(pk = True)
    name = fields.CharField(max_length=60)
    price = fields.FloatField()
    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'User', related_name='troskovi', index=True, null=False, on_delete=fields.CASCADE
    )


class Group(Model):
    class Meta:
        table = 'grupe'
        id_group = fields.UUIDField(pk=True)
        name_group = fields.CharField(max_length=60)




