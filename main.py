import sys
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from checker import ckecked

load_dotenv()


def get_sesion():

    mysql_connect = getenv("mysql_connect")

    engine = create_engine(mysql_connect, pool_recycle=3600)
    session_factory = sessionmaker(engine)

    session: Session = session_factory()
    return session


if __name__ == "__main__":
    ckecked(get_sesion(), sys.argv[1])
