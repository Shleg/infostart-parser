import os

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class SiteSettings(BaseSettings):
    username: SecretStr = os.getenv("username", None)
    password: SecretStr = os.getenv("password", None)
    username_1c: SecretStr = os.getenv("user1c", None)
    password_1c: SecretStr = os.getenv("pass1c", None)
