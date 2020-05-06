import datetime

import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    """Создаем базу данных"""
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False, pool_pre_ping=True)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)

    # creating sub
    session = create_session()
    if not session.query(__all_models.users.User).filter(__all_models.users.User.email == 'qwe@qwe').first():
        user = __all_models.users.User(
            name='qwe',
            email='qwe@qwe',
            confirmed=True,
            registered_on=datetime.datetime.now(),
            confirmed_on=datetime.datetime.now(),
            subscribe_date=datetime.date(2100, 1, 1)
        )
        user.set_password('qwe')
        session.add(user)
        session.commit()


def create_session() -> Session:
    global __factory
    return __factory()
