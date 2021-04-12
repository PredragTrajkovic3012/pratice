import json

from tortoise import Tortoise, fields
from tortoise.models import Model

#sta ce ovaj niz ovde???
models = ["Group", "User", "Trosak"]

class Group(Model):
    class Meta:
        table = 'grupe'
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=60)
    group_budget=fields.FloatField()

    users: fields.ReverseRelation["User"] = fields.ReverseRelation



class User(Model):
    class Meta:
        table = 'users'
        
    id = fields.UUIDField(pk = True)

    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50, null=True)
    monthly_income = fields.FloatField()

    group = fields.ForeignKeyField('models.Group', index=True, null=True, related_name='users')
   # troskovi: fields.ReverseRelation["Trosak"] = fields.ReverseRelation
    #nepotrebno jer dolazi iz troskova

    async def serialize(self, include_group=False, include_troskovi=False):
        user = {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        if include_group:
            await self.fetch_related('grupe')
            user['group'] = [g.name for g in self.group]

        if include_troskovi:
            await self.fetch_related('troskovi')
            user['troskovi'] = [await t.serialize() for t in self.troskovi]


        return user

    async def calc_budget_minus_trosak(self):


        await self.fetch_related("troskovi")
        await self.save()

        for t in self.troskovi:
            self.monthly_income = self.monthly_income - t.price

        await self.save()

        print(self.monthly_income)
        return self.monthly_income


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

    user = fields.ForeignKeyField('models.User', index=True,null=True, related_name='troskovi')

    async def serialize(self):
        return {
            'id': str(self.id),
            'id_user': str(self.user),
            'name': self.name,
            'price': self.price
        }

#    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
#        'User', related_name='troskovi', index=True, null=False, on_delete=fields.CASCADE
#    )

def db_url():
    with open('config.json', 'rt') as f:
        c = json.load(f)

    return f"postgres://{c['user']}:{c['password']}@{c['host']}/{c['dbname']}"




