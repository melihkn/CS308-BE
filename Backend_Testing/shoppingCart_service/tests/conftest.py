from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from ..models.models import Product, ShoppingCart
from sqlalchemy.orm import Session
from ..models.models import ShoppingCartItem, Customer
from ..models.models import Base

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
    db_session.query(Product).delete()
    db_session.query(ShoppingCart).delete()
    db_session.query(Customer).delete()
    db_session.query(ShoppingCartItem).delete()

    # Seed initial data for testing
    test_product = Product(
        product_id= "00000000-0000-0000-0000-000000000002",
        name="Test Product",
        model="Model-1",
        description="Test description",
        category_id=1,
        serial_number="SN12345",
        quantity=100,
        warranty_status=1,
        distributor="Test Distributor",
        price=9.99,
        cost=5.00,
        item_sold=0
    )
    test_cart = ShoppingCart(
        cart_id="00000000-0000-0000-0000-000000000004",
        customer_id="84037c94-99db-11ef-9ff5-80fa5b9b4ebf",
        cart_status="active"
    )
    test_customer = Customer(
        user_id="84037c94-99db-11ef-9ff5-80fa5b9b4ebf",
        name="John",
        surname="Doe",
        email="john.doe@example.com",
        password="hashedpassword",
    )
    test_cart_item = ShoppingCartItem(
        shopping_cart_item_id="00000000-0000-0000-0000-000000000003",
        cart_id="00000000-0000-0000-0000-000000000004",
        product_id="00000000-0000-0000-0000-000000000002",
        quantity=2,

    )
    db_session.add_all([test_product, test_cart, test_customer, test_cart_item])  # Add multiple objects at once

    db_session.commit()  # Save changes
    yield db_session  # Provide the session for the test
    # Seed additional data for testing


    db_session.commit()  # Save changes