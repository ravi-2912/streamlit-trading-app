import os
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from db.base import Base

load_dotenv()

ENCRYPTION_KEY = os.getenv("PASSWORD_ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY not set in environment or .env file.")
fernet = Fernet(ENCRYPTION_KEY.encode())


class AccountType(str, Enum):
    demo = "Demo"
    live = "Live"

class BrokerType(str, Enum):
    oanda = "Oanda"
    pepperstone = "Pepperstone"
    fxcm = "FXCM"
    ig = "IG"
    ftmo = "FTMO"
    the5ers = "The5ers"
    e8 = "E8"

class ServerType(str, Enum):
    mt5 = "MT5"
    mt4 = "MT4"
    ct5 = "cT5"

class Accounts(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    login = Column(String, nullable=True)
    __password_encrypted = Column("password", String, nullable=True)
    type = Column(SQLAlchemyEnum(AccountType), nullable=True)
    broker = Column(SQLAlchemyEnum(BrokerType), nullable=True)
    server = Column(SQLAlchemyEnum(ServerType), nullable=True)

    def __init__(self, **kwargs):
        password = kwargs.pop("password", None)
        super().__init__(**kwargs)
        if password is not None:
            self.password = password

    @property
    def password(self):
        if self.__password_encrypted:
            return fernet.decrypt(self.__password_encrypted.encode()).decode()
        return None

    @password.setter
    def password(self, value: str):
        if value:
            self.__password_encrypted = fernet.encrypt(value.encode()).decode()
        else:
            self.__password_encrypted = None

