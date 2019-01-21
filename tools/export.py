import csv

from pymongo import MongoClient


def calculate_price(user):
    price = 0
    if user['status'] == 'student':
        price += 65
    elif user['status'] == 'notStudent':
        price += 90
    if user['sillis'] == 'true':
        price += 15
    return price


client = MongoClient('localhost', 27017)
db = client.fuusio70
users = db.users.find()
with open('users.csv', 'w') as csvfile:
    fieldnames = list(users[0].keys()) + ['price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for user in users:
        user['price'] = calculate_price(user)
        writer.writerow(user)
