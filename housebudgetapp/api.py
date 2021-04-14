import json
import unittest
import asyncio
import uuid
import models
from models import User,Trosak,Group
from unittest.mock import patch
from tortoise.contrib.test import initializer, finalizer
from tortoise.transactions import in_transaction


async def add_user(first_name:str, last_name:str, monthly_income:float):
    user = User(first_name=first_name,
                 last_name=last_name, 
                 monthly_income=monthly_income)

    await user.save()

    return {'id': str(user.id)}

async def get_user_by_id(id_user:uuid.UUID):
    user = await User.filter(id=id_user).get_or_none()
    if not user:
        return {'status': 'error', 'message': 'not-found'}

    return {'first_name': user.first_name, 'last_name': user.last_name, 'balance': user.monthly_income}
            
async def add_spenses_for_user(id_user:uuid.UUID, spenses:list):

    async with in_transaction('models'):
    
      user = await User.filter(id=id_user).get_or_none()
      if not user:
          return {'status': 'error', 'message': 'not-found'}

      for t in spenses:
        db_t = Trosak(user=user, name=t['name'], price=t['price'])
        user.monthly_income -= t['price']
        await user.save()
        if user.monthly_income < 0:
            raise NameError("nema para na racunu")
            
        await db_t.save()

    
    return {'status': 'ok'}

async def get_trosak_by_id(id_trosak:uuid.UUID):
    trosak = await Trosak.filter(id=id_trosak).get_or_none()
    if not trosak:
        return {'status': 'error', 'message': 'not-found'}

    return {'name': trosak.name, 'price': trosak.price, 'user': trosak.user}

async def all_spenses_for_user(id_user:uuid.UUID):
    user = await User.filter(id=id_user).get_or_none()
    if not user:
        return {'status': 'error', 'message': 'not-found'}

    return {'status': 'ok', 'spenses': [{'name':s.name, 'price':s.price} for s in await Trosak.filter(user=user).all()]}

async def add_2users_in_Group(id_user1:uuid.UUID,id_user2:uuid.UUID,group_name:str):
    grupa1 = Group(name=group_name, group_budget=0.0)
    await grupa1.save()
    user1 = User(first_name='Predrag', last_name='Trajkovic', monthly_income=prihod1, group=grupa1)
    user2 = User(first_name='Milos', last_name='Copke', monthly_income=prihod2, group=grupa1)
    user3 = get_user_by_id(id_user1)

    #await  user1.save()
    #await user2.save()

    if user1.group == user2.group:
        grupa1.group_budget = user1.monthly_income + user2.monthly_income
        await  grupa1.save()
    # print(grupa1.group_budget);
    return grupa1.group_budget;
