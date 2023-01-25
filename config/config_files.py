import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

load_dotenv(find_dotenv())
@dataclass(frozen=True)
class APIkeys:
    private_key: str = os.getenv('account_key')
    account_name: str = os.getenv('account_name')