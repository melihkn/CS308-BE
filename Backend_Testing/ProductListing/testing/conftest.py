from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from ProductListing.main import app
from ProductListing.models.models import ProductDB, Category, Review, Customer, ProductPopularity, ProductManager

# Use SQLite for testing
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def db_session():
    from ProductListing.models.models import Base

    # Create all tables
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    yield session

    # Drop tables after the test
    session.close()
    Base.metadata.drop_all(bind=engine)

def print_database_content(db_session):
    print("Products:")
    for product in db_session.query(ProductDB).all():
        print(f"  {product}")

    print("Categories:")
    for category in db_session.query(Category).all():
        print(f"  {category}")

    print("Reviews:")
    for review in db_session.query(Review).all():
        print(f"  {review}")

    print("Product Managers:")
    for manager in db_session.query(ProductManager).all():
        print(f"  {manager}")



@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db(db_session):
    db_session.query(ProductDB).delete()
    db_session.query(Category).delete()
    db_session.query(Review).delete()
    db_session.query(ProductManager).delete()
    db_session.commit()

    # Seed the database
    categories = [
        Category(category_id=1, category_name="Dog Supplies"),
        Category(category_id=2, category_name="Cat Supplies"),
        Category(category_id=3, category_name="Aquatic Supplies"),
    ]
    products = [
        ProductDB(
            product_id="00000000-0000-0000-0000-000000000002",
            name="Dog Bed",
            model="DB-002",
            description="A comfortable dog bed",
            category_id=1,
            serial_number="SN-DOG-BED-002",
            quantity=10,
            price=60.00,
            cost=50.00,
            item_sold=5,
            warranty_status=None,
            distributor="PetShopCo",
            image_url="https://images.com/dog-bed.jpg",
        ),
    ]
    product_managers = [
        ProductManager(
            pm_id="00000000-0000-0000-0000-000000000003",
            name="John",
            middlename="Doe",
            surname="Smith",
            email="john.smith@example.com",
            password="hashedpassword",
            phone_number="1234567890",
        ),
    ]
    reviews = [
        Review(
            review_id="00000000-0000-0000-0000-000000000004",
            customer_id="00000000-0000-0000-0000-000000000001",
            product_id="00000000-0000-0000-0000-000000000002",
            rating=5,
            comment="Excellent product!",
            pm_id="00000000-0000-0000-0000-000000000003",
            approval_status="Approved",
        )
    ]

    db_session.bulk_save_objects(categories)
    db_session.bulk_save_objects(products)
    db_session.bulk_save_objects(product_managers)
    db_session.bulk_save_objects(reviews)
    db_session.commit()
    print_database_content(db_session)
    return db_session




@pytest.fixture(scope="function")
def client(setup_and_teardown_db):
    with TestClient(app) as test_client:
        yield test_client