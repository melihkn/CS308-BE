from schemas.categorySchemas import CategoryCreate
import pytest

def test_category_create_valid():
    data = {"category_name": "Electronics", "parentcategory_id": 1}
    category = CategoryCreate(**data)
    assert category.category_name == "Electronics"
    assert category.parentcategory_id == 1

def test_category_create_invalid():
    # Boş isim ve geçersiz türde parentcategory_id
    data = {"category_name": "", "parentcategory_id": "invalid"}
    with pytest.raises(ValueError):
        CategoryCreate(**data)

#DONE