import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

load_dotenv(find_dotenv())
@dataclass(frozen=True)
class vars:
    private_key: str = os.getenv('account_key')
    account_name: str = os.getenv('account_name')
    container_name: str = os.getenv('container_name')
    upload_folder: str = '/resources/'
    secret_key: str = os.getenv('secret_key')