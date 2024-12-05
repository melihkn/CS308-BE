import pytest
from fastapi.testclient import TestClient
from app import app
from unittest.mock import Mock
from dependencies import verify_pm_role, oauth2_scheme

# Mock Token Fixture
@pytest.fixture(scope="module")
def mock_token():
    """
    Testlerde kullanılmak üzere mock bir Authorization token sağlar.
    """
    return "test_token"

# Mock verify_pm_role Dependency
@pytest.fixture(scope="module", autouse=True)
def mock_verify_pm_role():
    """
    verify_pm_role bağımlılığını mock ederek tüm kimlik doğrulama kontrollerini bypass eder.
    """
    mock_function = Mock(return_value=True)
    app.dependency_overrides[verify_pm_role] = mock_function
    yield
    app.dependency_overrides.pop(verify_pm_role)

# Mock oauth2_scheme Dependency (Eğer token doğrulama gerekiyor ise)
@pytest.fixture(scope="module", autouse=True)
def mock_oauth2_scheme():
    """
    oauth2_scheme bağımlılığını mock ederek tüm token doğrulama kontrollerini bypass eder.
    """
    mock_function = Mock(return_value="mocked_user")
    app.dependency_overrides[oauth2_scheme] = mock_function
    yield
    app.dependency_overrides.pop(oauth2_scheme)

# Mock SQLAlchemy Session
@pytest.fixture(scope="function")
def mock_db_session():
    """
    Testler için mock bir veritabanı oturumu sağlar.
    """
    mock_session = Mock()
    yield mock_session

# TestClient Fixture
@pytest.fixture(scope="module")
def client():
    """
    FastAPI uygulamanıza HTTP istekleri yapmak için TestClient sağlar.
    """
    with TestClient(app) as test_client:
        yield test_client