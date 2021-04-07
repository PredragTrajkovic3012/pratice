from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from models import *
import utils
import csv

async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    c = {
        'user' : 'predrag',
        'password' : '123',
        'host' : 'localhost',
        'dbname' : 'housebudgetapp'
    }
    await Tortoise.init(
        db_url=f"postgres://{c['user']}:{c['password']}@{c['host']}/{c['dbname']}",
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

    grupa1 = Group(id_group=utils.generate_uuid4(), name_group="Braca na praksi")
    losmi = User(id=utils.generate_uuid4(), first_name='Losmi', last_name='Copara', monthly_income=20000,group=grupa1.id)
    predrag=User(id=utils.generate_uuid4()+"", first="Predragoslav",last_name="Trajkovic",monthly_income=30000,group=grupa1.id)
    trosak1=Trosak(id_trosak=utils.generate_uuid4(),name="Struja",price=5000,user=losmi.id)




    #trosak1 = Trosak()


    await losmi.save()
    # with open('MOCK_DATA.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     next(reader)
    #     for row in reader:
    #         predrag = User(id=utils.generate_uuid4(), first_name=row[1] + "", last_name=row[2] + "",
    #                        monthly_income=(float(row[3])))
    #         await predrag.save()

run_async(init())
