import contextlib
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session

def get_db1():
    engine=create_engine('mysql+mysqlconnector://root:@localhost/laplanduas_rental')
    db_session = sessionmaker(bind=engine)
    session=db_session()
    return session

@contextlib.contextmanager
def get_db():
    _db=None
    try:
        engine=create_engine('mysql+mysqlconnector://root:@localhost/laplanduas_rental')
        db_session = sessionmaker(bind=engine)
        _db=db_session()
        print("######## yield db")
        yield _db
    finally:
        if _db is not None:
            print("######## all done closing db connection")
            _db.close()


#Aina kun tietotyyppiä DW käytetään routehandlerissa avataan yhteys ja kun ei tarvita se sulkee sen automaattisesti
engine2=create_engine('mysql+mysqlconnector://root:@localhost/laplanduas_rental')
dw_session=sessionmaker(bind=engine2)

def get_dw():
    _dw=None
    try:
        _dw= dw_session()
        yield _dw
    finally:
        if _dw is not None:
            _dw.close()



DW = Annotated[Session,Depends(get_dw)]