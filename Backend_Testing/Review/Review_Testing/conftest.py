import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..review_models.models import Base
from ..dbContext_Review import engine, Base

# Replace this with your actual database URL
DATABASE_URL = "mysql+pymysql://root:lokmata23@127.0.0.1:3306/myvet_db" 
import pytest
from ..review_models.models import Base  # Replace with the correct path

from sqlalchemy import Column, Integer, String


class MockCategory(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..review_models.models import Base  # Replace with your actual models module

# Define your database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """
    Set up and tear down the database state for each test.
    This uses a transactional approach to isolate each test.
    """
    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(bind=connection)
    yield session  # Provide the session to tests
    session.rollback()
    session.close()
    transaction.rollback()  # Roll back all changes made during the test
    connection.close()


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)  # Ensure tables exist
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()  # Rollback changes after each test
    session.close()


