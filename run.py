import os

from app import create_app
from config import ProductionConfig as DefaultConfig

Config = os.getenv('APP_CONFIG', DefaultConfig)

app = create_app(Config)

if __name__ == '__main__':
    app.run()
