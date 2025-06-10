from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


from app.database import Base # Import your Base
# Add imports for all your models here so Alembic can discover them
from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.option import Option
from app.models.user_answer import UserAnswer
from app.models.user_progress import UserProgress

# Add environment variable loading for Alembic
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), '.env')) # Load .env relative to CWD

from app.config import settings # Import your settings


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Add this to use your DATABASE_URL from settings
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not a connection object.  By default, the URL is taken from the alembic.ini file.
    Here we override it to use the DATABASE_URL from our settings.
    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario, we need to create a connection
    to the database in order to acquire a database lock.
    """
    connectable = engine_from_config(
        {
            "sqlalchemy.url": settings.DATABASE_URL,
            "sqlalchemy.poolclass": pool.NullPool, # Pass the actual class object, not its string name
        },
        prefix="sqlalchemy.",
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
