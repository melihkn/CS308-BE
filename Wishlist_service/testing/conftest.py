import pytest
from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dbContext import Base, get_db
from fastapi.testclient import TestClient
from main import app
from models.models import Wishlist, WishlistItem, Product, Customer, Base
from sqlalchemy.orm.session import Session


# Replace with your database URL
# Replace with your database URL
DATABASE_URL = "sqlite:///:memory:"

# Create the engine
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function", autouse=True)
def db_session():
    """
    SQLAlchemy session started with SAVEPOINT.
    After the test, roll back to this SAVEPOINT.
    """
    # Establish a connection and start a transaction
    connection = engine.connect()
    trans = connection.begin()  # Non-ORM transaction
    session = sessionmaker(bind=connection)()

    session.begin_nested()  # Start a SAVEPOINT

    # Listen for the end of SAVEPOINT and reopen it
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, transaction):
        if transaction.nested and not transaction._parent.nested:
            sess.begin_nested()

    yield session  # Provide the session to the test

    # Cleanup after test
    session.close()
    trans.rollback()  # Roll back to the SAVEPOINT
    connection.close()

    
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db(db_session: Session):
    """
    Cleans up the database and seeds test data before each test.
    """
    # Cleanup all rows from the tables
    db_session.query(Customer).delete()
    db_session.query(Product).delete()
    
    db_session.query(Wishlist).delete()
    db_session.query(WishlistItem).delete()

    db_session.commit()
    


    test_customer = Customer(
        user_id="84037c94-99db-11ef-9ff5-80fa5b9b4ebf",
        name="Test User1",
        surname="Test Surname",
        email="test@example.com",
        password="hashedpassword"
    )

    test_wishlist = Wishlist(
        wishlist_id="840416fd-99db-11ef-9ff5-80fa5b9b4ebf",
        customer_id="84037c94-99db-11ef-9ff5-80fa5b9b4ebf",
        name="Test Wishlist1",
        wishlist_status="active"
    )
    
    test_product = Product(
        product_id="84041531-99db-11ef-9ff5-80fa5b9b4ebf",
        name="Test Product1",
        model="Model-X",
        description="A test product",
        serial_number="SN12345",
        quantity=50,
        warranty_status=1,
        distributor="Test Distributor",
        price=100.00,
        item_sold=0,
    )

    test_product2 = Product(
        product_id="84042531-99db-11ef-9ff5-80fa5b9b4ebg",
        name="Test Product2",
        model="Model-Y",
        description="A test product",
        serial_number="SN123456",
        quantity=50,
        warranty_status=1,
        distributor="Test Distributor",
        price=100.00,
        item_sold=0,
    )
    test_wishlist_item = WishlistItem(
        wishlist_item_id="84031531-99db-11ef-9ff5-80fa5b9b4ebf",
        wishlist_id="840416fd-99db-11ef-9ff5-80fa5b9b4ebf",
        product_id="84041531-99db-11ef-9ff5-80fa5b9b4ebf"
    )

    db_session.add_all([test_customer,test_wishlist, test_product, test_product2, test_wishlist_item])
    db_session.commit()
    yield db_session


    db_session.commit()

