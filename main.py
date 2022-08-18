import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, drop_tables, Publisher, Book, Shop, Stock, Sale

from secret_file import BD, LOGIN, PASSWORD


DSN = '{}://{}:{}@localhost:5432/PythonORM'.format(BD, LOGIN, PASSWORD)
engine = sqlalchemy.create_engine(DSN)
drop_tables(engine)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open("tests_data.json", "rb") as f:
    data = json.load(f)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
inp_pulblisher = input("Введите имя или id издателя: ")
if inp_pulblisher.isdigit():
    q = session.query(Shop).join(Stock.shops).join(Book).join(Publisher).\
        filter(Publisher.id == inp_pulblisher)
else:
    q = session.query(Shop).join(Stock.shops).join(Book).join(Publisher). \
        filter(Publisher.name == inp_pulblisher)
for item in q.all():
    print(item.id, item.name)
session.close()

#Почему такой вариант не работает?
#table_name = (item['model']).title()
#session.add(table_name(id=item.get('pk'), **item.get('fields')))