import sys
import os

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.categoryServices import create_category_, get_categories

def test_create_category():
    # Örnek bir kategori oluşturma testi
    category_data = {"category_name": "Test Category", "parentcategory_id": None}
    result = create_category_(category_data)
    assert result.category_name == "Test Category"
    assert result.parentcategory_id is None

def test_get_categories():
    # Örnek tüm kategorileri listeleme testi
    categories = get_categories()
    assert isinstance(categories, list)