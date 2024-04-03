from abc import ABC, abstractmethod


class BaseClient(ABC):
    @abstractmethod
    def get_my_friends(self) -> list[str]:
        raise NotImplementedError


class FacebookClient(BaseClient):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_my_friends(self) -> list[str]:
        # Rzeczywiste odczytanie znajomych z facebooka przez wyslanie zapytania http
        # Musisz sie poalczyc z serwerem fb i pobrac informacje

        return ["prawdziwy_znajomy1", "prawdziwy_znmajomy2"]


class MockedClient(BaseClient):
    def __init__(self):
        pass

    def get_my_friends(self) -> list[str]:
        # Zwroci nam "oszukana" liste przyjaciol
        friends = ["sztuczny_znajomy1", "sztuczny_znajomy2"]
        return friends


def foo(client: BaseClient):
    pass


if __name__ == "__main__":
    mocked_client = MockedClient()
    real_client = FacebookClient("kuba", "pass123")
