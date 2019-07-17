def test_home_page(client):
    assert client.get('/')
