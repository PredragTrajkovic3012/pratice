from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from models import *
from tortoise.transactions import in_transaction
import utils
import csv

async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    c = {
        'user' : 'predrag',
        'password' : '123',
        'host' : '127.0.0.1',
        'dbname' : 'housebudgetapp'
    }
    await Tortoise.init(
        db_url=f"postgres://{c['user']}:{c['password']}@{c['host']}/{c['dbname']}",
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

    grupa1 = Group(name="Braca na praksi",group_budget=0.0)
    await grupa1.save()


    losmi = User(first_name='Losmi', last_name='Copara', monthly_income=20000, group=grupa1)
    predrag=User(first_name="Predragoslav",last_name="Trajkovic",monthly_income=30000,group=grupa1)





    async with in_transaction():
        await losmi.save()
        await predrag.save()

    trosak = Trosak(name="Struja", price=5000, user=predrag)

    async with in_transaction():
        await trosak.save()

    await grupa1.fetch_related('users')
    for user in grupa1.users:
        print(user)

    

#    trosak1=Trosak(id_trosak=utils.generate_uuid4(),name="Struja",price=5000,user=losmi.id)




    #trosak1 = Trosak()


#    await losmi.save()
    # with open('MOCK_DATA.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     next(reader)
    #     for row in reader:
    #         predrag = User(id=utils.generate_uuid4(), first_name=row[1] + "", last_name=row[2] + "",
    #                        monthly_income=(float(row[3])))
    #         await predrag.save()

if __name__=="__main__":
    run_async(init())

