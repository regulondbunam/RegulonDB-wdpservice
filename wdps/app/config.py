from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde .env
load_dotenv()

class Config:
    GRAPHQL_URL = os.getenv('GRAPHQL_URL')