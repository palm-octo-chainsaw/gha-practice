from src.hello import hello


def test_hello_message():
    assert hello() == "Hello, Actions!"
