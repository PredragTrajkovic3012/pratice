import json
import unittest
import asyncio
import uuid
import models
from models import User,Trosak,Group
from unittest.mock import patch
from tortoise.contrib.test import initializer, finalizer

import api

class test_BaseTestCase(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'rt') as f:
            c = json.load(f)

        asyncio.set_event_loop(None)
        self.loop = asyncio.new_event_loop()

        initializer(
            modules={"models": models},
            loop=self.loop,
            db_url=models.db_url(),
        )

    def tearDown(self):
        _flush_db = not hasattr(self, 'flush_db_at_the_end') or self.flush_db_at_the_end
        if _flush_db:
            finalizer()

async def  dodaj_usera_i_trosak():
    user1 = User(first_name='Predrag',last_name='Trajkovic', monthly_income=20000)
    await user1.save()

    trosak=Trosak(name="Struja",price=2000)
    await trosak.save()



    return str(user1.id), str(trosak.id)

async def  dodaj_usere_i_trosak_calc_budget(user_budget,trosak):


    trosak=Trosak(name="Struja",price=trosak)
    await trosak.save()


    user1 = User(first_name='Predrag', last_name='Trajkovic', monthly_income=user_budget)
    await user1.save()
    trosak.user = user1
    await trosak.save()
    await user1.fetch_related("troskovi")
    await user1.save()


    for t in user1.troskovi:
        user1.monthly_income=user1.monthly_income-t.price


    await user1.save()
#    print(user1.monthly_income)
    return user1.monthly_income

async def  dodaj_usera_i_troskove_calc_budget(user_budget,trosk):


    user1 = User(first_name='Predrag', last_name='Trajkovic', monthly_income=user_budget)
    await user1.save()
    for tr in trosk:
        tr.user=user1
        await tr.save()

    await user1.fetch_related("troskovi")
    await user1.save()


    #for t in user1.troskovi:
        #user1.monthly_income=user1.monthly_income-t.price
    await  user1.calc_budget_minus_trosak()


    await user1.save()
    #print(user1.monthly_income)
    return user1.monthly_income



async def  users_in_group_Budget_merge_budget(prihod1,prihod2):
    grupa1 = Group(name="NoHomo",group_budget=0.0)
    await grupa1.save()
    user1 = User(first_name='Predrag', last_name='Trajkovic', monthly_income=prihod1,group=grupa1)
    user2 = User(first_name='Milos', last_name='Copke', monthly_income=prihod2,group=grupa1)
    await  user1.save()
    await user2.save()


    if user1.group == user2.group:

        grupa1.group_budget = user1.monthly_income+user2.monthly_income
        await  grupa1.save()
    #print(grupa1.group_budget);
    return grupa1.group_budget;




class MyTestCase(test_BaseTestCase):

    def test_add_user_and_a_few_spenes(self):
        
        res = self.loop.run_until_complete(api.add_user("Pera", "Peric", 5000))
        self.assertTrue('id' in res)
        id_user = res['id']

        self.assertEqual({'balance': 5000.0, "first_name":"Pera","last_name":"Peric"}, self.loop.run_until_complete(api.get_user_by_id(id_user)))
        
        extra_spenses=[{'name': 'struja','price': 300},
                 {'name': 'voda','price': 100},
                 {'name': 'kurve','price': 4500},
                 {'name': 'grejanje','price': 500}]

        spenses=[{'name': 'struja','price': 300},
                 {'name': 'voda','price': 100},
                 {'name': 'grejanje','price': 500}]
        
        self.assertEqual({'status':'ok'},
                         self.loop.run_until_complete(api.add_spenses_for_user(id_user, spenses)))

        self.assertEqual({'status': 'ok', 'spenses': [{'name': 'struja', 'price': 300.0}, {'name': 'voda', 'price': 100.0}, {'name': 'grejanje', 'price': 500.0}]},
                         self.loop.run_until_complete(api.all_spenses_for_user(id_user)))

        self.assertEqual({'balance': 5000-300-100-500, "first_name":"Pera","last_name":"Peric"}, self.loop.run_until_complete(api.get_user_by_id(id_user)))

        with self.assertRaises(NameError):
            self.loop.run_until_complete(api.add_spenses_for_user(id_user, extra_spenses))
        
        self.flush_db_at_the_end = False
    
    def test_add_user_and_fetch_user_by_id(self):
        res = self.loop.run_until_complete(api.add_user("Pera", "Peric", 70000))
        self.assertTrue('id' in res)
        id_user = res['id']
        self.assertEqual({"first_name":"Pera","last_name":"Peric"}, self.loop.run_until_complete(api.get_user_by_id(id_user)))

    def test_add_user_and_try_to_fetch_non_existing_user(self):
        res = self.loop.run_until_complete(api.add_user("Pera", "Peric", 70000))
        self.assertTrue('id' in res)

        id_user = '00000000-0000-0000-0000-000000000001'
        self.assertEqual({'status': 'error', 'message': 'not-found'}, self.loop.run_until_complete(api.get_user_by_id(id_user)))

    def test_add_usr_and_trosak(self):
        id_user, id_trosak = self.loop.run_until_complete(dodaj_usera_i_trosak())

    def test_UserBudget_minus_Trosak(self):
       self.assertEqual(18000, self.loop.run_until_complete(dodaj_usere_i_trosak_calc_budget(20000,2000)))

    def test_UserBudget_minus_Troskovi(self):
        t1 = Trosak(name="Struja", price=2000)
        t2 = Trosak(name="Za Dete", price=5000)
        arrayTroskovi=[t1,t2]
        self.assertEqual(13000, self.loop.run_until_complete(dodaj_usera_i_troskove_calc_budget(20000,arrayTroskovi)))


    def test_UserBudget_merge(self):

        self.assertEqual(25000,self.loop.run_until_complete(users_in_group_Budget_merge_budget(10000,15000)))




if __name__ == '__main__':
    unittest.main()
