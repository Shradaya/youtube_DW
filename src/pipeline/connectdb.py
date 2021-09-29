import os
from dotenv import load_dotenv
load_dotenv()

def connect(psy):
    return psy.connect(
        host = os.getenv('host'),
        database = os.getenv('db1'),
        user = os.getenv('user'),
        password = os.getenv('password'),
        port = os.getenv('port')
    )

    
