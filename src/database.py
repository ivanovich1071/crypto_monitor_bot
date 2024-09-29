from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker

# Инициализация базы данных
engine = create_engine('sqlite:///users.db')
metadata = MetaData()

users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('chat_id', Integer, unique=True, nullable=False),
                    Column('thresholds', String)  # Хранение в виде запятой-отделённых значений
                    )


def init_db():
    metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def add_user(chat_id):
    existing_user = session.query(users_table).filter_by(chat_id=chat_id).first()
    if not existing_user:
        ins = users_table.insert().values(chat_id=chat_id, thresholds='')
        session.execute(ins)
        session.commit()


def update_user_thresholds(chat_id, threshold):
    user = session.query(users_table).filter_by(chat_id=chat_id).first()
    if user:
        current_thresholds = set(map(int, user.thresholds.split(','))) if user.thresholds else set()
        if threshold in current_thresholds:
            current_thresholds.remove(threshold)
        else:
            current_thresholds.add(threshold)
        updated_thresholds = ','.join(map(str, sorted(current_thresholds, reverse=True)))
        upd = users_table.update().where(users_table.c.chat_id == chat_id).values(thresholds=updated_thresholds)
        session.execute(upd)
        session.commit()


def get_user_thresholds(chat_id):
    user = session.query(users_table).filter_by(chat_id=chat_id).first()
    if user and user.thresholds:
        return sorted(map(int, user.thresholds.split(',')), reverse=True)
    return []


def get_all_users():
    users = session.query(users_table).all()
    user_list = []
    for user in users:
        thresholds = list(map(int, user.thresholds.split(','))) if user.thresholds else []
        user_list.append({
            'chat_id': user.chat_id,
            'thresholds': thresholds
        })
    return user_list
