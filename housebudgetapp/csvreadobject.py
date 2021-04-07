import csv
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from models import *
import utils
with open('MOCK_DATA.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:


        predrag = User(id=utils.generate_uuid4(), first_name=row[1]+"", last_name=row[2]+"", monthly_income=(float(row[3])))
        #await predrag.save()
        #print(predrag)



