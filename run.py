import os

from app import create_app
from config import Config as DefaultConfig

Config = os.getenv('APP_CONFIG', DefaultConfig)

app = create_app(Config)

if __name__ == '__main__':
    app.run()
