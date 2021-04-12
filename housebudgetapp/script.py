import csv
from faker import Faker
import uuid
from random import randrange
import utils

fake = Faker()

Troskovi = ["Struja","Voda","Komunalije","Teretana","Kupovina","Popravka Auta","Za bebu","Kupovina pljuga",
          "Popravka Cevi","Rucak u restoranu","Pravljenje torte","Rodjendan","Alkohol","Gorivo","Karte za koncert"
          "Kupovina knjiga","WC papir","Hemija"]

with open('users.csv', mode='w') as users_file:
    users_writer = csv.writer(users_file, delimiter=',')

    for r in range(0, 500):
        users_writer.writerow([utils.generate_uuid4(),fake.first_name(),fake.last_name(),fake.random_int()])


with open('troskovi.csv', mode='w') as troskovi_file:
    troskovi_writer = csv.writer(troskovi_file, delimiter=',')

    for r in range (0,500):
        troskovi_writer.writerow([utils.generate_uuid4(),Troskovi[randrange(0,len(Troskovi))],fake.random_int()])