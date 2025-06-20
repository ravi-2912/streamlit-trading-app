import os
from sqlalchemy import Column, Integer, String
from db.base import Base
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = os.getenv("PASSWORD_ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY not set in environment or .env file.")
fernet = Fernet(ENCRYPTION_KEY.encode())

SEVER_TYPE = ["MetaTrader 5"]
ACOUNT_TYPE = ["Demo", "Live"]
ACCOUNT_FROM = ["Oanda", "IC Markets", "Pepperstone", "FXCM", "IG", "FTMO", "The5ers", "E8"]

class Accounts(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    login = Column(String, nullable=True)
    _password = Column(String, nullable=True)
    type = Column(String, nullable=True)
    account_from = Column(String, nullable=True)
    server_type = Column(String, nullable=True)


    # Secure password interface
    @property
    def password(self):
        if self._password:
            return fernet.decrypt(self._password.encode()).decode()
        return None

    @password.setter
    def password(self, value):
        self._password = fernet.encrypt(value.encode()).decode()

