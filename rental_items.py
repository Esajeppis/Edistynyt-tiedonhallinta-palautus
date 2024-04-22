from random import choice
import uuid
from faker import Faker

import faker_commerce
from sqlalchemy import text
from db import get_db
from categories import get_categories
from users import get_users

def _get_items(_db):
    _query= "SELECT id from rental_items"
    ids=[]
    rows=_db.execute(text(_query))
    for row in rows:
        ids.append(row[0])
    return ids


def insert_features():
    with get_db() as _db:
        _query = "INSERT INTO features(features) VALUES(:features)"
        for _feature in ['material','size', 'price','color']:
            try:
                _db.execute(text(_query), {'features':_feature})
                _db.commit()
            except Exception as e:
                print(e)
                _db.rollback()

def insert_items():
    with get_db() as _db:
        fake=Faker()
        fake.add_provider(faker_commerce.Provider)
        categories = get_categories(_db)
        _query = "INSERT INTO rental_items(name,description,created_at, serial_number,categories_id) VALUES"
        variables = {}
        for i in range(1000):
            _query += f'(:name{i}, :desc{i}, :created_at{i}, :sn{i},:categories_id{i}),'
            variables[f'name{i}']=fake.ecommerce_name()
            variables[f'desc{i}']=fake.text()
            variables[f'created_at{i}']=fake.date()
            variables[f'sn{i}']= str(uuid.uuid4())
            variables[f'categories_id{i}']=choice(categories)
        _query=_query[:-1]
        _db.execute(text(_query),variables)
        _db.commit()

def _get_features(_db):
    _query= "SELECT id,features FROM features"
    _features=[]
    rows=_db.execute(text(_query))
    for row in rows:
        _features.append({'id':row[0], 'features':row[1]})
    return _features


def mix_features_and_items():
    fake=Faker()
    fake.add_provider(faker_commerce.Provider)
    colors=['black','cyan','yellow','white','red','pink']
    sizes = ['XXS','XS','S','M','L','XL','XXL','XXXL','20x30','70x3000']

    with get_db() as _db:
        items = _get_items(_db)
        features = _get_features(_db)

        _query="INSERT INTO rental_items_has_features(rental_items_id,features_id,value) VALUE(:item_id,:features_id,:value)"
        for i in range(1000):
            try:
                item_id=choice(items)
                for f in features:
                    if f['features']== 'color':
                        value=choice(colors)
                    elif f['features']=='price':
                        value=fake.ecommerce_price(False)
                    elif f['features']=='size':
                        value=choice(sizes)
                    elif f['features']=='material':
                        value=choice(faker_commerce.PRODUCT_DATA['material'])
                    _db.execute(text(_query),{'item_id':item_id,'features_id': f['id'], 'value': value})
                    _db.commit()

            except Exception as e:
                print(e)
                _db.rollback()

def rent_items():
    with get_db() as _db:
        fake = Faker()
        users = get_users(_db)
        items = _get_items(_db)
        _query = "INSERT INTO rental_transaction(created_at, due_date, auth_users_id, rental_items_id) VALUES"
        variables= {}
        for i in range(1000):
            _query += f'(:created_at{i}, :due_date{i}, :auth_users_id{i}, :rental_items_id{i}),'
            variables[f'created_at{i}'] = fake.date()
            variables[f'due_date{i}']=fake.date()
            variables[f'auth_users_id{i}']=choice(users)
            variables[f'rental_items_id{i}']=choice(items)
        _query = _query[:-1]
        _db.execute(text(_query), variables)
        _db.commit()