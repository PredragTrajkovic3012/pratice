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

async def all_spenses_for_user(id_user:uuid.UUID):
    user = await User.filter(id=id_user).get_or_none()
    if not user:
        return {'status': 'error', 'message': 'not-found'}

    return {'status': 'ok', 'spenses': [{'name':s.name, 'price':s.price} for s in await Trosak.filter(user=user).all()]}    