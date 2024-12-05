from unittest.mock import Mock
from services.categoryServices import create_category_, get_categories

def test_create_category(mock_db_session):
    # Mock kategori verisi
    mock_category_data = Mock(category_name="Books", parentcategory_id=None)

    # Fonksiyonu çağır
    result = create_category_(mock_db_session, mock_category_data)

    # Mock session'daki işlemleri kontrol et
    mock_db_session.add.assert_called_once_with(result)
    mock_db_session.commit.assert_called_once()

    # Dönen sonucun doğruluğunu kontrol et
    assert result.category_name == "Books"

def test_get_categories(mock_db_session):
    # Mock dönüş verisi
    mock_db_session.query.return_value.all.return_value = [{"id": 1, "name": "Books"}]

    # Fonksiyonu çağır
    result = get_categories(mock_db_session)

    # Dönen sonuçları kontrol et
    assert len(result) == 1
    assert result[0]["name"] == "Books"

#DONE