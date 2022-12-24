import environ
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False)
)
PROJECT_ROOT_DIR = Path(__file__).resolve().parent

# Take environment variables from .env file
environ.Env.read_env(PROJECT_ROOT_DIR / '.env')
