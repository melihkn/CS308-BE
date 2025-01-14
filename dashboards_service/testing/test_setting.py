import sys
import os

# settings.py modül yolunu ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from settings import settings

def test_settings_load():
    """
    Ayarların doğru yüklendiğini test et.
    """
    assert settings.jwt_secret is not None
    assert settings.database_url.startswith("sqlite://")