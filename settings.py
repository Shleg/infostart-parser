import os

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr

load_dotenv()


class SiteSettings(BaseSettings):
    username: SecretStr = os.getenv("username", None)
    password: SecretStr = os.getenv("password", None)
