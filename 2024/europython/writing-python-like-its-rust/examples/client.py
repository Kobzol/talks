from collections.abc import Iterator
from contextlib import contextmanager


class Client:
    def __init__(self, address: str):
        self.address = address

    def send(self, data):
        pass


@contextmanager
def connect(address: str) -> Iterator[Client]:
    client = Client(address)
    try:
        yield client
    except:
        close_client(client)


def close_client(client: Client):
    pass
